from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import MyUserManager


class MyCustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=60, unique=True)
    company_name = models.CharField(max_length=225)
    phone = models.CharField(max_length=20, unique=True)
    profile = models.ImageField(upload_to='user/', null=True, blank=True)
    contry = models.CharField(max_length=50)
    fullname = models.CharField(max_length=30)
    date_joined = models.DateTimeField(auto_now_add=True)  # auto_now_add updates on creation only
    last_login = models.DateTimeField(auto_now=True)  # auto_now updates field each time
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ['fullname', 'phone']  # fields user has to fill

    objects = MyUserManager()

    def _str_(self):
        return self.fullname

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
