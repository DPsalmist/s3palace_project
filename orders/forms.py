from django import forms
from .models import Order
#from django.utils.translation import ugettext_lazy as _
   
class OrderCreateForm(forms.ModelForm):
    #postal_code = USZipCodeField()
    
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'street_address', 'phone_no', 'postal_code', 'city', 'state']
	