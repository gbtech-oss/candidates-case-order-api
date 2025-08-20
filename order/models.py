
from django.db import models



class DeliveryAddress(models.Model):
	street_name = models.CharField(max_length=255)
	number = models.CharField(max_length=20)
	complement = models.CharField(max_length=255, blank=True, null=True)
	reference_point = models.CharField(max_length=255, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.street_name}, {self.number}"


class Order(models.Model):
	client_name = models.CharField(max_length=300)
	client_document = models.CharField(max_length=14)
	delivery_date = models.DateField()
	delivery_address = models.OneToOneField(DeliveryAddress, on_delete=models.CASCADE, related_name='order', blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"Pedido {self.id} - {self.client_name}"

	class Meta:
		unique_together = ('client_name', 'client_document', 'delivery_date')



class Item(models.Model):
	order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
	name = models.CharField(max_length=255)
	quantity = models.PositiveIntegerField()
	unit_price = models.DecimalField(max_digits=10, decimal_places=2)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.name} (x{self.quantity})"
