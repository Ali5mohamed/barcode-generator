from django import forms
from .models import Barcode

class BarcodeForm(forms.ModelForm):
    class Meta:
        model = Barcode
        fields = ['type', 'title', 'description', 'url', 'product_image']
        widgets = {
            'type': forms.Select(attrs={'class':'form-select'}),
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
            'url': forms.URLInput(attrs={'class':'form-control'}),
            'product_image': forms.FileInput(attrs={'class':'form-control'}),
        }
