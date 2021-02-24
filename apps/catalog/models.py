from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
from mptt.models import MPTTModel, TreeForeignKey

from utils.models import BaseModel
from .helpers import get_brand_upload_path, get_category_upload_path, get_product_upload_path


class Banner(BaseModel):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='banners')
    thumbnail = ImageSpecField(source='image',
                               processors=[ResizeToFit(360, 240)],
                               format='JPEG',
                               options={'quality': 60})
    link = models.URLField(blank=True)
    placement = models.ForeignKey(
        'BannerPlacement',
        related_name='banners',
        on_delete=models.CASCADE,
        null=True,
        blank=True
        )
    from_time = models.DateTimeField(blank=True, null=True)
    to_time = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class BannerPlacement(BaseModel):
    name = models.CharField(max_length=30, unique=True, blank=True)

    def __str__(self):
        return self.name


class Brand(BaseModel):
    manufacturer = models.ForeignKey(
        'Manufacturer',
        related_name='brands',
        on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name='brand')
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=get_brand_upload_path, blank=True)
    thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(250, 250)],
        format='JPEG',
        options={'quality': 70}
    )
    meta_title = models.CharField(max_length=150, blank=True)
    meta_description = models.TextField(max_length=160, blank=True)
    meta_keyword = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = clean_str(self.slug, lower=True)
        super().save(*args, **kwargs)


class Manufacturer(BaseModel):
    name = models.CharField(max_length=255, verbose_name='manufacturer')

    def __str__(self):
        return self.name


class Category(MPTTModel, BaseModel):
    parent = TreeForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='children',
        db_index=True,
        on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name='category')
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to=get_category_upload_path, blank=True)
    thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(250, 250)],
        format='JPEG',
        options={'quality': 70})
    meta_title = models.CharField(max_length=150, blank=True)
    meta_description = models.TextField(max_length=160, blank=True)
    meta_keyword = models.CharField(max_length=300, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/c/{self.slug}'

    def save(self, *args, **kwargs):
        self.slug = clean_str(self.slug, lower=True)

        # If parent is not active, set child as not active as well
        if not self.is_active:
            children = self.get_descendants(include_self=False)
            for child in children:
                child.is_active = False
                child.save()

        super().save(*args, **kwargs)

    def get_active_children(self):
        # Returns queryset containing immediate active children, in tree order
        if hasattr(self, '_cached_children'):
            qs = self._tree_manager.filter(
                pk__in=[n.pk for n in self._cached_children],
                is_active=True
            )
            qs._result_cache = self._cached_children
            return qs

        return (
            self._tree_manager.none()
            if self.is_leaf_node()
            else self._tree_manager._mptt_filter(parent=self, is_active=True))


class Product(BaseModel):
    brand = models.ForeignKey(
        'Brand',
        related_name='products',
        on_delete=models.PROTECT)
    category = models.ForeignKey(
        'Category',
        related_name='products',
        on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    search_alias = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    sku = models.CharField(max_length=50, unique=True, verbose_name='SKU')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)
    meta_title = models.CharField(max_length=150, blank=True)
    meta_description = models.TextField(max_length=160, blank=True)
    meta_keyword = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Clean and generate internal codes
        self.slug = clean_str(self.slug, lower=True)
        super().save(*args, **kwargs)