from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from django.urls import reverse
from shop.models import Suits, Category
from cart.cart import Cart
#from .tasks import order_created
import time

# Paypal payment gateway 
def order_create(request):
    cart = Cart(request)
    categories = Category.objects.all()

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        # create transaction id
        transaction_id = int(round(time.time() * 1000))
        new_transaction_id = f's3p-{transaction_id}'
        print("Order transacton id is: ", new_transaction_id)
        # Get total order cost
        total_order_cost = cart.get_total_price()
        new_total_order_cost = float(total_order_cost)
        print('Total oder cost is ', total_order_cost)

        if form.is_valid():
        	obj = form.save(commit=False)
        	obj.order_transaction_id = transaction_id 
        	order = form.save()
        	for item in cart:
	            OrderItem.objects.create(order=order,product=item['product'],price=item['price'], quantity=item['quantity'])
	       	cart.clear()

	       	# set session
	       	request.session['order_transaction_id'] = new_transaction_id
	       	request.session['order_cost'] = new_total_order_cost
	       	
	       	return redirect(reverse('orders:order_created'))
    else:
        form = OrderCreateForm()
    return render(request,'orders/order/create.html',{'cart': cart, 'form': form, 'categories': categories,})


def order_created(request):
	cart = Cart(request)
	# get session data
	order_transaction_id = request.session['order_transaction_id']
	total_order_cost = request.session['order_cost']
	categories = Category.objects.all()
	context = {'cart':cart, 'order_id':order_transaction_id, 'total_order_cost':total_order_cost, 'categories': categories}
	return render(request, 'orders/order/created.html', context )