import os


def get_brand_upload_path(instance, filename):
    return os.path.join('brands', str(instance.id), filename)


def get_category_upload_path(instance, filename):
    return os.path.join('categories', str(instance.id), filename)


def get_product_upload_path(instance, filename):
    return os.path.join('products', str(instance.product_id), filename)
