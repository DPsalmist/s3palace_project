from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Suits, Category
from .cart import Cart
from .forms import CartAddProductForm, CartUpdateProductForm
   
@require_POST
def cart_add(request, prod_id):
	cart = Cart(request)
	product = get_object_or_404(Suits, id=prod_id)
	form = CartAddProductForm(request.POST)
	print('This is the cart:',cart)
	print('This is the product from the cart view:', product, product.image.url)

	if form.is_valid():
		cd = form.cleaned_data
		cart.add(product=product,quantity=cd['quantity'],override_quantity=cd['override'])
	return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, prod_id):
    cart = Cart(request)
    suit = get_object_or_404(Suits, id=prod_id)
    suit_det = get_object_or_404(Suits, id=prod_id, available=True)
    cart.remove(suit)
    return redirect('cart:cart_detail')

def cart_detail(request, category_slug=None):
    cart = Cart(request)
    category = None
    categories = Category.objects.all()
    suits = Suits.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        suits = suits.filter(category=category)
        
    for item in cart:
        item['update_quantity'] = CartAddProductForm(initial={
			'quantity':item['quantity'],
			'override': True})#item_update_form = CartUpdateProductForm()
    print('This is the cart detail:',cart)
    
    context = {
		'category': category,
        'suits':suits,
        'categories': categories,
        'cart': cart
     }
    return render(request, 'cart/cart_detail.html', context) 