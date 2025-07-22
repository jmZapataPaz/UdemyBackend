from django.urls import path
from .views import create_address, get_address_by_user, delete_address, update_address

urlpatterns = [
    path('', create_address),
    path('user/<int:id_user>', get_address_by_user),
    path('<int:id_address>', delete_address),
    path('update/<int:id_address>', update_address),
]