from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from .models import Product


class ProductList(ListView):
    model = Product
    context_object_name = 'users'  # Default: object_list
    paginate_by = 10
    # queryset = Product.objects.all()  # Default: Model.objects.all()


class ProductDetailView(DetailView):
    model = Product

    def product_detail_view(request, primary_key):
        product = get_object_or_404(Product, pk=primary_key)
        return render(request, 'product_detail.html', context={'product': product})
