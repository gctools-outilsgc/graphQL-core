from django.db import models
from .helpers import unique_filepath


class Profile(models.Model):
    gcID = models.CharField(unique=True, max_length=100)
    first_name = models.CharField(null=False, blank=False, max_length=50)
    last_name = models.CharField(null=False, blank=False, max_length=75)
    email = models.EmailField(max_length=255, unique=True)
    avatar = models.ImageField(upload_to=unique_filepath, null=True, blank=True)
    mobile_phone = models.CharField(null=True, blank=True, max_length=15)
    office_phone = models.CharField(null=True, blank=True, max_length=15)
    address = models.ForeignKey('Address', null=True, on_delete=models.CASCADE)
    title_en = models.CharField(null=False, blank=False, max_length=150)
    title_fr = models.CharField(null=False, blank=False, max_length=150)
    supervisor = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    org = models.ForeignKey('OrgTier', null=True, blank=True, on_delete=models.SET_NULL)


class Address(models.Model):
    street_address = models.CharField(null=False, blank=False, max_length=100)
    city = models.CharField(null=False, blank=False, max_length=100)
    province = models.CharField(null=False, blank=False, max_length=100)
    postal_code = models.CharField(null=False, blank=False, max_length=10)
    country = models.CharField(null=False, blank=False, max_length=100, default='Canada')


class OrgTier(models.Model):
    name_en = models.CharField(null=False, blank=False, max_length=150)
    name_fr = models.CharField(null=False, blank=False, max_length=150)
    ownerID = models.ForeignKey(Profile, null=False, blank=False, on_delete=models.ProtectedError)








