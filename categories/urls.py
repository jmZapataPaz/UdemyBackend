from django.urls import path
from .views import create, get_categories, delete, update

urlpatterns = [
    path('', create),
    path('getCategories', get_categories),
    path('delete/<int:id_category>', delete),
    path('update/<int:id_category>', update),
]
