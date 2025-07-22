from django.db import models

# Create your models here.
class OrderHasProducts (models.Model):
    id_product = models.ForeignKey('products.Product', on_delete=models.CASCADE, db_column='id_product')
    id_order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, db_column='id_order')
    quantity = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order_has_products'
        unique_together = ('id_product', 'id_order')
        
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.ForeignKey('users.User', on_delete=models.CASCADE, db_column='id_user')
    id_address = models.ForeignKey('address.Address', on_delete=models.CASCADE, db_column='id_address')
    status = models.CharField(max_length=255, default='PAGADO')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    products = models.ManyToManyField(
        'products.Product',
        through='orders.OrderHasProducts',
        related_name='products'
    )
    
    class Meta:
        db_table = 'orders'
    