from django.urls import path
from users.views import update, updateWithImage, get_user_by_id, get_all_users, remove_role_from_user, assign_role_to_user, get_all_roles

urlpatterns = [
    path('get/<id_user>', get_user_by_id),
    path('get_all', get_all_users),
    path('<id_user>', update),
    path('upload/<id_user>', updateWithImage),
    path('assign_role/<id_user>', assign_role_to_user),
    path('remove_role/<id_user>/<role_id>', remove_role_from_user),
    path('roles/', get_all_roles),    
]
