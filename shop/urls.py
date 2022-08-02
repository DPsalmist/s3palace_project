from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
	path('', views.home, name='home'),
	path('about/', views.about, name='about'),
	path('contact/', views.contact, name='contact'),
	path('search/', views.search, name='search'),
	path('gallery/', views.gallery, name='gallery'),
	path('<int:id>/<slug:slug>/', views.suit_detail,name='suit_detail'),
	path('suits/<slug:category_slug>/', views.category_list,name='product_list_by_category'),
]
