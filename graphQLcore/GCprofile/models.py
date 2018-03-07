from django.db import models
from .helpers import unique_filepath


class Profile(models.Model):
    gcID = models.CharField(unique=True, max_length=100)
    name = models.CharField(null=False, blank=False, max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    avatar = models.ImageField(upload_to=unique_filepath, null=True, blank=True)
    mobile_phone = models.CharField(null=True, blank=True, max_length=15)
    office_phone = models.CharField(null=True, blank=True, max_length=15)
    address = models.ForeignKey('Address', null=True, on_delete=models.SET_NULL)
    title_en = models.CharField(null=True, blank=True, max_length=150)
    title_fr = models.CharField(null=True, blank=True, max_length=150)
    supervisor = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name="Employees")
    org = models.ForeignKey('OrgTier', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Address(models.Model):
    street_address = models.CharField(null=False, blank=False, max_length=100)
    city = models.CharField(null=False, blank=False, max_length=100)
    province = models.CharField(null=False, blank=False, max_length=100)
    postal_code = models.CharField(null=False, blank=False, max_length=10)
    country = models.CharField(null=False, blank=False, max_length=100, default='Canada')

    def __str__(self):
        return u'%s %s' % (self.street_address, self.city)


class OrgTier(models.Model):
    name_en = models.CharField(null=False, blank=False, max_length=150)
    name_fr = models.CharField(null=False, blank=False, max_length=150)
    department = models.ForeignKey('Department', null=False, blank=False, on_delete=models.CASCADE, related_name="Org_Tiers")
    ownerID = models.ForeignKey('Profile', null=True, blank=False, on_delete=models.SET_NULL, related_name="Owner_of_Org_Tiers")

    def __str__(self):
        return u'%s / %s' % (self.name_en, self.name_fr)


class Department(models.Model):
    name_en = models.CharField(null=False, blank=False, max_length=150)
    name_fr = models.CharField(null=False, blank=False, max_length=150)
    acronym_fr = models.CharField(null=False, blank=False, max_length=10)
    acronym_en = models.CharField(null=False, blank=False, max_length=10)

    def __str__(self):
        return u'%s / %s' % (self.acronym_en, self.acronym_fr)









