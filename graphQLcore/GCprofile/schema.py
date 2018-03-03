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


class ProfileOptionalInput(graphene.InputObjectType):
    avatar = graphene.String(required=False, default_value=None)
    mobile_phone = graphene.String(required=False, default_value=None)
    office_phone = graphene.String(required=False, default_value=None)
    address_id = graphene.Int(required=False, default_value=None)
    supervisor_gc_id = graphene.String(required=False, default_value=None)
    org_id = graphene.Int(required=False, default_value=None)


class CreateProfile(graphene.Mutation):
    gcID = graphene.String()
    name = graphene.String()
    email = graphene.String()
    title_en = graphene.String()
    title_fr = graphene.String()
    avatar = graphene.String()
    mobile_phone = graphene.String()
    office_phone = graphene.String()
    address = graphene.Field(AddressType)
    supervisor = graphene.Field(ProfileType)
    org = graphene.Field(OrgTierType)

    class Arguments:
        gc_id = graphene.String()
        name = graphene.String()
        email = graphene.String()
        title_en = graphene.String()
        title_fr = graphene.String()
        optional_data = ProfileOptionalInput(required=False)

    def mutate(self, info, gc_id, name, email, title_en, title_fr, optional_data=None):

        profile = Profile(
            gcID=gc_id,
            name=name,
            email=email,
            title_en=title_en,
            title_fr=title_fr,
        )

        if optional_data is None:
            profile.address = None
            profile.supervisor = None
            profile.org = None
        else:
            profile.avatar = optional_data.avatar
            profile.mobile_phone = optional_data.mobile_phone
            profile.office_phone = optional_data.office_phone

            if optional_data.address_id is None:
                profile.address = None
            else:
                profile.address = Address.objects.filter(id=optional_data.address_id).first()
                if not profile.address:
                    raise Exception('Invalid Address')
            if optional_data.supervisor_gc_id is None:
                profile.supervisor = None
            else:
                profile.supervisor = Profile.objects.filter(gcID=optional_data.supervisor_gc_id).first()
                if not profile.supervisor:
                    raise Exception('Invalid Supervisor Entry')
            if optional_data.org_id is None:
                profile.org = None
            else:
                profile.org = OrgTier.objects.filters(id=optional_data.org_id).first()

        profile.save()

        return CreateProfile(
            gcID=profile.gcID,
            name=profile.name,
            email=profile.email,
            avatar=profile.avatar,
            mobile_phone=profile.mobile_phone,
            office_phone=profile.office_phone,
            address=profile.address,
            title_en=profile.title_en,
            title_fr=profile.title_fr,
            supervisor=profile.supervisor,
            org=profile.org,)


class Query(graphene.ObjectType):
    profiles = graphene.List(ProfileType, search=graphene.String())
    addresses = graphene.List(AddressType)
    orgtiers = graphene.List(OrgTierType)
    departments = graphene.List(DepartmentType)

    def resolve_profiles(self, info, search=None, **kwargs):
        if search is not None:
            filter = (
                Q(name__icontains=search)
            )
            return Profile.objects.filter(filter)
        return Profile.objects.all()

    def resolve_addresses(self, info, **kwargs):
        return Address.objects.all()

    def resolve_orgtiers(self, info, **kwargs):
        return OrgTier.objects.all()

    def resolve_departments(self, info, **kwargs):
        return Department.objects.all()


class Mutation(graphene.ObjectType):
    create_profile = CreateProfile.Field()
