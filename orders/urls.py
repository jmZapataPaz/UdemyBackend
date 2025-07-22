from django.urls import path
from .views import create_order, get_orders_by_user,update_order,get_orders
urlpatterns = [
    path('', create_order),
    path('user/<int:id_user>', get_orders_by_user),
    path('<int:id_order>', update_order),
    path('all', get_orders),
    
    
]
