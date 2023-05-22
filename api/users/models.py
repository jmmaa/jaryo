from django.db import models
from django_countries.fields import CountryField

# Create your models here.


class User(models.Model):
    # login credentials
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    email_address = models.EmailField()

    # personal info
    fullname = models.CharField(max_length=256, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    country = CountryField(blank=True, null=True)
    birthday = models.DateTimeField(blank=True, null=True)
    # country_code (theoretically, this should be already defined when choosing a country)

    # image (i dont know how to implement this correctly...)

    # social links (soon)

    def save(self, *args, **kwargs):
        super().full_clean()
        super().save(*args, **kwargs)


class RefreshToken(models.Model):
    token = models.CharField(max_length=256)
