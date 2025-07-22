from django.db import models

# Create your models here.
class Address(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        db_column='id_user',
        related_name='users'
    )
    address = models.CharField(max_length=255)
    neighborhood = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'address'
    