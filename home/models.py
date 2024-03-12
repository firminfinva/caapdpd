from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from decimal import Decimal
from django.utils import timezone
from django.conf import settings

import random
import os


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, is_staff=False, is_active=True, is_admin=False):
        if not phone:
            raise ValueError('users must have a phone number')
        if not password:
            raise ValueError('users must have a password')

        user_obj = self.model(
            phone=phone
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,

        )
        return user

    def create_superuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user


# otp_policy = str(En m"'"inscrivant, je suis conscient que detofa ne vendra ni ne partagera mes données avec aucune autre entreprise, uniquement pour son propre usage. )

class User(AbstractBaseUser, PermissionsMixin):
    SEX = (('Homme', 'Homme'),
           ('Femme', 'Femme'),)

    PROV = (
        ('Bas-Uele', 'Bas-Uele'),
        ('Équateur', 'Équateur'),
        ('Haut-Katanga', 'Haut-Katanga'),
        ('Haut-Lomami', 'Haut-Lomami'),
        ('Haut-Uele', 'Haut-Uele'),
        ('Ituri', 'Ituri'),
        ('Kasaï', 'Kasaï'),
        ('Kasaï central', 'Kasaï central',),
        ('Kasaï oriental', 'Kasaï oriental'),
        ('Kinshasa', 'Kinshasa'),
        ('Kongo-Central', 'Kongo-Central'),
        ('Kwango', 'Kwango'),
        ('Kwilu', 'Kwilu'),
        ('Lomami', 'Lomami'),
        ('Lualaba', 'Lualaba'),
        ('Mai-Ndombe', 'Mai-Ndombe'),
        ('Maniema', 'Maniema'),
        ('Mongala', 'Mongala'),
        ('Nord-Kivu', 'Nord-Kivu'),
        ('Nord-Ubangi', 'Nord-Ubangi'),
        ('Sankuru', 'Sankuru'),
        ('Sud-Kivu', 'Sud-Kivu'),
        ('Sud-Ubangi', 'Sud-Ubangi'),
        ('Tanganyika', 'Tanganyika'),
        ('Tshopo', 'Tshopo'),
        ('Tshuapa', 'Tshuapa'),
    )

    VILLE = (('Bukavu', 'Bukavu'),
             ('Butembo', 'Butembo'),
             ('Goma', 'Goma'),
             ('Kinshasa', 'Kinshasa'),
             ('Lubumbashi', 'Lubumbashi'),)
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True, default='Votre nom')
    phone_regex = RegexValidator(
        regex=r'^(\+\d{1,3})?,?\s?\d{9,13}$',
        message="Le numéro de téléphone doit être saisi au format : '+243...'.jusqu'à 14 chiffres autorisés")
    phone = models.CharField(
        validators=[phone_regex], max_length=15, unique=True, default='+243')
    # province = models.CharField(max_length=200, null=False, choices=PROV, default='Nord-Kivu')
    email = models.EmailField(max_length=254, null=False, default='@gmail.com')
    ville = models.CharField(max_length=100, null=False, choices=VILLE, default='Goma')
    sexe = models.CharField(max_length=20, null=False, choices=SEX, default='Homme')
    age = models.DateField(null=True, blank=True, default='2002-01-14')
    image = models.ImageField(default="placeholder.png", null=True, blank=True)
    active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    timeatamp = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)


    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    objects = UserManager()

    def get_full_name(self):
        if self.username:
            return self.phone
        else:
            return self.phone

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):  # __unicode__ on Python 2
        return self.phone

    def birthday(self):
        import datetime
        return int((datetime.date.today() - self.birthday).days / 365.25)

    def has_perm(self, perm, obj=None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        # "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        # "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        # "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        #  "Is the user active?"
        return self.active

    class Meta:
        ordering = ['-date']





class LoggedInUser(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, related_name='logged_in_user', on_delete=models.CASCADE)
    session_key = models.CharField(max_length=32, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.user.username


class ResetPassword(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    lien = models.CharField(max_length=100, default="lien")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
