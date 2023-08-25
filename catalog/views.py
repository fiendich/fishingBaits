from django.views.generic import ListView
from .models import Lure, Color
from .forms import BrandFilterForm



class LureCatalogView(ListView):
    model = Lure
    template_name = 'catalog.html'
    context_object_name = 'lures'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        brand_filter_form = BrandFilterForm(self.request.GET)

        if brand_filter_form.is_valid() and brand_filter_form.cleaned_data['brand']:
            queryset = queryset.filter(brand=brand_filter_form.cleaned_data['brand'])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brand_filter_form'] = BrandFilterForm(self.request.GET)
        return context


