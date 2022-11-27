from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Category
import re

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'slug')

    name = forms.CharField(
        label_suffix=" **",
        label="Category Name",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    slug = forms.SlugField(
        label_suffix=" **",
        label="Cetegory Slug",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    def clean_name(self, *args, **kwargs):
        name = self.cleaned_data.get("name")
        if name == "":
            raise forms.ValidationError(_("Category name can not be blank"))
        else:
            return name

    def clean_slug(self, *args, **kwargs):
        slugName    = self.cleaned_data.get("slug")
        if slugName == "":
            raise forms.ValidationError(_("Category slug can not be blank,"))
        else:
            return slugName
