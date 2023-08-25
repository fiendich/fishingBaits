from django.urls import path
from .views import LureCatalogView

urlpatterns = [
    path('', LureCatalogView.as_view(), name='lure_catalog'),
]
