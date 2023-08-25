from django.urls import path
from contacts import views


urlpatterns = [
    # ...
    path('contacts/', views.contact_view, name='contacts'),
    # ...
]