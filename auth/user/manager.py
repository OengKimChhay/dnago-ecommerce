from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
from django.utils.translation import gettext_lazy as _


class MyUserManager(BaseUserManager):
    def create_user(self, email, fullname, password=None, **other_fields):
        if not email:
            raise ValueError(_("email is required"))
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            fullname=fullname,
            **other_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, fullname, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(_('Super user must have is_staff true'))

        if other_fields.get('is_superuser') is not True:
            raise ValueError(_('Super user must have is_superuser true'))

        return self.create_user(
            email,
            password,
            fullname,
            **other_fields
        )
