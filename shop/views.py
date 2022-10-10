from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Suits, Category, Gallery, Review
from cart.forms import CartAddProductForm
from django.core.mail import BadHeaderError, send_mail, EmailMessage
from django.db.models import Q 
from cart.cart import Cart
from django.conf import settings
from .forms import ReviewForm

# Create your views here.
def home(request):
	category = None
	categories = Category.objects.all()
	all_suits = Suits.objects.filter(available=True)
	suits = Suits.objects.filter(available=True).order_by('created')[:12]
	last_suit = Suits.objects.filter(available=True).last()
	cart = Cart(request)
	penultimate_suit = Suits.objects.filter(available=True).order_by('-created')[0:1]
	pen_suit = penultimate_suit[0]
                       
	#Category Filters
	chinese_suits = all_suits.filter(category__id__exact=2).order_by('-created')[0:3]
	italian_suits = all_suits.filter(category__id__exact=1).order_by('-created')[0:3]
	turkey_suits = all_suits.filter(category__id__exact=3).order_by('-created')[0:3],

	context = {
		'category': category,
        'last_suit':last_suit,
        'pen_suit':pen_suit,
        'suits':suits,
        'categories': categories,
        'cart': cart,
        'italian_suits':italian_suits,
        'chinese_suits':chinese_suits,
        'turkey_suits':turkey_suits
   		}

	return render(request,'shop/product/index.html', context)


def about(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    suits = Suits.objects.filter(available=True)
    cart = Cart(request)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        suits = suits.filter(category=category)
    
    context = {
		'category': category,
        'suits':suits,
        'cart': cart,
        'categories': categories
     }
    return render(request, 'shop/product/about.html', context)


def gallery(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    suits = Suits.objects.filter(available=True)
    gallery = Gallery.objects.all()
    cart = Cart(request)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        suits = suits.filter(category=category)
    
    context = {
        'category': category,
        'gallery':gallery,
        'cart': cart,
        'suits':suits,
        'categories': categories
     }
    return render(request, 'shop/product/gallery.html', context)


def contact(request):
    cart = Cart(request)
    categories = Category.objects.all()
    context = {'categories':categories, 'cart':cart}
    # Validate contact form 
    if request.method == 'POST':
        # Get details from the form
        fullname = request.POST['fullname']
        print('contact name;', fullname)
        phone_no = request.POST['phonenumber']
        contact_email = request.POST['email']
        message = request.POST['message']
    
        #subject = 'A New Message From SeamlessBuy Store'
        contact_message = f'S3Palace New Message, \n\n' \
                f'Hi! You have a message from {fullname} with details below. \n' \
                f'Phone Number: {phone_no} \n' \
                f'Message: {message}.'

        email_msg = EmailMessage(
            subject="Message From S3Palace", body=contact_message,
            from_email=contact_email,
            to=[settings.EMAIL_HOST_USER],
            headers={'Reply-To': contact_email})
        email_msg.send()
        #messages.success(request, f'Thank you for contacting us! We\'ll get back to you soon.')
        return redirect ('shop:home')
    return render(request, 'shop/product/contact.html', context)


def suit_detail(request, id, slug):
    suit = get_object_or_404(Suits, id=id, slug=slug, available=True)
    categories = Category.objects.all()
    cart_product_form = CartAddProductForm()
    print('This is suit detail=', suit)
    cart = Cart(request)

    # List of active reviews for this post
    reviews = suit.reviews.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            # Create Comment object but don't save to db yet
            new_review = review_form.save(commit=False)
            new_review.product = suit
            new_review.save()
    else:
        review_form = ReviewForm()

    context = {
		'suit': suit,
        'categories':categories,
        'cart':cart,
		'cart_product_form': cart_product_form,
        'review_form':review_form,
        'reviews':reviews
	}
    return render(request,'shop/product/suit_detail.html',context)


def category_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    suits = Suits.objects.filter(available=True)
    cart = Cart(request)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        suits = suits.filter(category=category)
    
    for a in suits:
        print('This is suit:',a, a.get_absolute_url)
        
    context = {
		'category': category,
        'suits':suits,
        'cart':cart,
        'categories': categories
        }
    return render(request,'shop/product/suit_category_list.html', context)

def search(request):
    # get search query
    search_query = request.GET.get('q')
    categories = Category.objects.all()
    cart = Cart(request)
    print('search object: ', search_query)
    suits = Suits.objects.filter(Q(name__icontains=search_query) | Q(category__name__icontains=search_query)).filter(available=True).order_by('created')
    print('returned search results = ', suits)
    context = {'suits':suits, 'search_query':search_query, 'categories':categories, 'cart':cart}

    return render(request, 'shop/product/search_results.html', context)