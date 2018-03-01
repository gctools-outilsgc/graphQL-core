import graphene
from graphene_django import DjangoObjectType
from .models import Profile, Address, OrgTier, Department
from django.db.models import Q

class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile


class AddressType(DjangoObjectType):
    class Meta:
        model = Address


class OrgTierType(DjangoObjectType):
    class Meta:
        model = OrgTier


class DepartmentType(DjangoObjectType):
    class Meta:
        model = Department


class Query(graphene.ObjectType):
    profiles = graphene.List(ProfileType, search=graphene.String())
    addresses = graphene.List(AddressType)
    orgtiers = graphene.List(OrgTierType)
    departments = graphene.List(DepartmentType)

    def resolve_profiles(self, info, search=None, **kwargs):
        if search:
            profile_filter = (
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        return Profile.objects.filter(profile_filter)

    def resolve_addresses(self, info, **kwargs):
        return Address.objects.all()

    def resolve_orgtiers(self, info, **kwargs):
        return OrgTier.objects.all()

    def resolve_departments(self, info, **kwargs):
        return Department.objects.all()
