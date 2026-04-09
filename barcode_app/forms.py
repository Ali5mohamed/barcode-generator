from django import forms
from .models import Barcode , Link , Product

class BarcodeForm(forms.ModelForm):
    class Meta:
        model = Barcode
        fields = ['title',]
        widgets = {
            'type': forms.Select(attrs={'class':'form-select'}),
            'title': forms.TextInput(attrs={'class':'form-control'}),
            # 'price': forms.TextInput(attrs={'class':'form-control'}),
            #'description': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
            #'url': forms.URLInput(attrs={'class':'form-control'}),
            # 'product_image': forms.FileInput(attrs={'class':'form-control'}),
        }
class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['url', 'description']
        widgets = {
            
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'price': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
            'image': forms.FileInput(attrs={'class':'form-control'}),
        }


# from django import forms
# from .models import Barcode, Link

# class BarcodeForm(forms.ModelForm):
#     class Meta:
#         model = Barcode
#         fields = ['title', 'description', 'price', 'product_image']
#         widgets = {
#             'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'أدخل عنوان الباركود'}),
#             'description': forms.Textarea(attrs={'class':'form-control', 'rows':3, 'placeholder':'الوصف'}),
#             'price': forms.TextInput(attrs={'class':'form-control', 'placeholder':'السعر'}),
#             'product_image': forms.FileInput(attrs={'class':'form-control'}),
#         }

# class LinkForm(forms.ModelForm):
#     class Meta:
#         model = Link
#         fields = ['url', 'description']
#         widgets = {
#             'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder':'رابط الموقع'}),
#             'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder':'وصف الرابط'}),
#         }