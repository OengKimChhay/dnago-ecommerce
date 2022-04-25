from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import MyCustomUser
import re

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
PHONE_REGEX = r"^\+?1?\d{9,15}$"
SPECIAL_CHAR_REGEX = "[@_!#$%^&*()<>?/\|}{~:]"


class UserForm(UserCreationForm):
    class Meta:
        model = MyCustomUser
        fields = (
            'fullname',
            'phone',
            'email',
            'company_name',
            'contry',
            'password1',
            'password2',
            'profile',
            'is_admin',
            'is_customer',
            'is_verified',
            'is_staff',
        )
    fullname = forms.CharField(
        label="Full Name",  # show label name
        label_suffix=" **",  # show next to label
        required=False,  # remove required attr
        # strip=False,   # False mean accept backspace
        widget=forms.TextInput(
            attrs={
                "placeholder": "Full Name",
                "class": "form-control"
            }
        )
    )

    phone = forms.CharField(
        label_suffix=" **",
        label="Phone",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Phone",
                "class": "form-control",
                "rows": "5"
            }
        )
    )

    email = forms.EmailField(
        label_suffix=" **",
        label="Email",
        required=False,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Example@gmail.com",
                "class": "form-control"
            }
        )
    )

    company_name = forms.CharField(
        label_suffix=" **",
        label="Company Name",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Company Name",
                "class": "form-control",
            }
        )
    )

    contry = forms.CharField(
        label_suffix=" **",
        label="Contry Name",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Contry Name",
                "class": "form-control",
            }
        )
    )

    password1 = forms.CharField(
        label_suffix=" **",
        label="Password",
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ),
        help_text="Your password can’t be too similar to your other personal information.Your password must contain at least 6 characters.Your password can’t be a commonly used password.Your password can’t be entirely numeric.",
    )

    password2 = forms.CharField(
        label_suffix=" **",
        label="Re-Password",
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Re-Password",
                "class": "form-control"
            }
        ),
        help_text="Enter the same password as before, for verification."
    )

    profile = forms.FileField(
        label_suffix=" **",
        label="Profile",
        required=False,
        widget=forms.FileInput(
            attrs={
                "placeholder": "Profile Pic",
                "class": "form-control",
            }
        )
    )

    is_admin = forms.BooleanField(
        label_suffix=" **",
        label="Admin",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
            }
        )
    )

    is_customer = forms.BooleanField(
        label_suffix=" **",
        label="Customer",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input"
            }
        )
    )

    is_verified = forms.BooleanField(
        label_suffix=" **",
        label="Verify",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input"
            }
        )
    )

    is_staff = forms.BooleanField(
        label_suffix=" **",
        label="Staff",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
            }
        )
    )

    # ----------- validation -----------------
    # ------------ the clean func is for global error not in the feilds form --------------------
    # def clean(self):
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 is not None:
    #         if password1 != password2:
    #             raise forms.ValidationError(
    #                 "Password and Re-password does not match"
    #             )

    def clean_fullname(self, *args, **kwargs):
        fullname = self.cleaned_data.get("fullname")
        if fullname == "":
            raise forms.ValidationError(_("Full Name can not be blank"))
        else:
            return fullname

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        if email == "":
            raise forms.ValidationError(_("Employee Email can not be blank"))
        elif MyCustomUser.objects.filter(email__iexact=email).exclude(email=email):
            raise forms.ValidationError(_("Email already exists. try another one"))
        elif email and not re.match(EMAIL_REGEX, email):
            raise forms.ValidationError(_('Invalid email format, example@gmail.com'))
        else:
            return email

    def clean_company_name(self, *args, **kwargs):
        company_name = self.cleaned_data.get("company_name")
        if company_name == "":
            raise forms.ValidationError(_("Company name can not be blank"))
        else:
            return company_name

    def clean_contry(self, *args, **kwargs):
        contry = self.cleaned_data.get("contry")
        if contry == "":
            raise forms.ValidationError(_("Contry can not be blank"))
        else:
            return contry

    def clean_phone(self, *args, **kwargs):
        phone = self.cleaned_data.get("phone")
        if phone == "":
            raise forms.ValidationError(_("Phone can not be blank"))
        elif phone and not re.match(PHONE_REGEX, phone):
            raise forms.ValidationError(_('invalid phone number.'))
        else:
            return phone

    def clean_password1(self, *args, **kwargs):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        fullname = self.cleaned_data.get("fullname")
        email = self.cleaned_data.get("email")
        if password1 == "":
            raise forms.ValidationError(_("Password can not be blank"))
        elif len(password1) <= 5:
            raise forms.ValidationError(_("Password must be more then 5 characters"))
        elif password1 == fullname:
            raise forms.ValidationError(_("Password is too similar to the full name"))
        elif password1 == email:
            raise forms.ValidationError(_("Password is too similar to the email"))
        elif password1 and not re.compile(SPECIAL_CHAR_REGEX).search(password1):
            raise forms.ValidationError(_('Password must contain special characters'))
        # elif password1 != password2:
        #     raise forms.ValidationError(_("Re Password not match"))
        else:
            return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 is not None:
            if password2 == "" or password1 != password2:
                raise forms.ValidationError(
                    "Password and Re-password does not match"
                )
