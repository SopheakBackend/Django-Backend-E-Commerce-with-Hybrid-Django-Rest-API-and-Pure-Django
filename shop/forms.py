# shop/forms.py
from django import forms
from parler.forms import TranslatableModelForm
from .models import Product

class ProductForm(TranslatableModelForm):
    class Meta:
        model = Product
        # Include all editable fields. Parler automatically handles name, slug, and description inside here!
        fields = ['category', 'name', 'slug', 'description', 'image', 'price', 'available']
        
        # Style fields to match your base.css form styling rules
        widgets = {
            'category': forms.Select(attrs={'style': 'width: 324px; padding: 10px; border-radius: 4px; background: #efefef; border: 0; margin-bottom: 10px;'}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'available': forms.CheckboxInput(attrs={'style': 'width: auto; float: none; clear: none; margin-bottom: 0;'}),
        }
