# coding: utf8
from PIL import Image
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)



class ProfileManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):

        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Profile(AbstractBaseUser):
    email = models.EmailField(verbose_name='E-mail address', max_length=255, unique=True,)
    full_name = models.CharField(verbose_name='Full name', max_length=30, null=True, blank=True)
    nick_name = models.CharField(verbose_name='Nickname', max_length=30, null=True, blank=True, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    country = models.CharField(verbose_name='Country', max_length=30, null=True, blank=True)
    city = models.CharField(verbose_name='City', max_length=30, null=True, blank=True)
    photo = models.ImageField(upload_to='profiles/%Y/%m/%d/', verbose_name='Фото', blank=True, null=True)
    about_me = models.TextField(verbose_name='About me', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = ProfileManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['full_name', 'nick_name']

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super(Profile, self).save(*args, **kwargs)
        if self.photo:
            wanted_dim = 250
            file = self.photo.path
            height = self.photo.height
            width = self.photo.width
            if width != wanted_dim:
                max_side = max(height, width)
                k = wanted_dim / max_side
                new_width = round(width * k)
                new_height = round(height * k)
                picture = Image.open(file)
                picture = picture.resize((new_width, new_height), Image.ANTIALIAS)
                picture.save(file)

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
