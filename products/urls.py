from django.urls import path
from .views import create,get_products_by_category, delete_by_id_product, update_by_id_product

urlpatterns = [
    path('', create),
    path('category/<int:id_category>', get_products_by_category), 
    path('<int:id_product>', delete_by_id_product),
    path('update/<int:id_product>', update_by_id_product), 
]
