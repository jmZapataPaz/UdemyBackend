from django.urls import path
from .views import create, get_categories, delete

urlpatterns = [
    path('', create),
    path('getCategories', get_categories),
    path('delete/<int:id_category>', delete),
]
