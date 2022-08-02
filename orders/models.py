from django.db import models
from shop.models import Suits
from decimal import Decimal

   
class Order(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.EmailField()
	phone_no = models.IntegerField(null=True)
	street_address = models.CharField(max_length=250)
	postal_code = models.CharField(max_length=20)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100, null=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	paid = models.BooleanField(default=False)
	order_transaction_id = models.CharField(max_length=200, blank=True)

	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return f'Order {self.id}'

	def get_total_cost(self):
    		return Decimal(sum(item.get_cost() for item in self.items.all()))
'''
	def get_total_cost(self):
		total_cost = sum(item.get_cost() for item in self.items.all())
		return total_cost - total_cost * \
			(self.discount / Decimal(100))'''
			#return sum(item.get_cost() for item in self.items.all())
	


class OrderItem(models.Model):
	order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
	product = models.ForeignKey(Suits,related_name='order_items', on_delete=models.CASCADE)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField(default=1)

	def __str__(self):
		return str(self.id)

	def get_cost(self):
		return Decimal(self.price) * Decimal(self.quantity)
		#return self.price * self.quantity

	