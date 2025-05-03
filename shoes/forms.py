from django import forms
from .models import Shoe

class ShoeForm(forms.ModelForm):
    class Meta:
        model = Shoe
        fields = ['name', 'description', 'price', 'category', 'image', 'stock', 'is_featured']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class CartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)
