from django.urls import path
from users.views import update, updateWithImage, get_user_by_id, get_all_users

urlpatterns = [
    path('get/<id_user>', get_user_by_id),
    path('get_all', get_all_users),
    path('<id_user>', update),
    path('upload/<id_user>', updateWithImage)  
]
