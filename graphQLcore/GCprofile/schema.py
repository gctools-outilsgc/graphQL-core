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
    title_en = graphene.String(required=False, default_value=None)
    title_fr = graphene.String(required=False, default_value=None)
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
        optional_data = ProfileOptionalInput(required=False)

    @staticmethod
    def mutate(self, info, gc_id, name, email, title_en, title_fr, optional_data=None):

        profile = Profile(
            gcID=gc_id,
            name=name,
            email=email,
        )

        if optional_data is None:
            profile.address = None
            profile.supervisor = None
            profile.org = None
        else:
            profile.avatar = optional_data.avatar
            profile.mobile_phone = optional_data.mobile_phone
            profile.office_phone = optional_data.office_phone
            profile.title_fr = optional_data.title_fr
            profile.title_en = optional_data.title_en

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


class CreateDepartment(graphene.Mutation):
    name_en = graphene.String()
    name_fr = graphene.String()
    acronym_fr = graphene.String()
    acronym_en = graphene.String()

    class Arguments:
        name_en = graphene.String()
        name_fr = graphene.String()
        acronym_fr = graphene.String()
        acronym_en = graphene.String()

    @staticmethod
    def mutate(self, info, name_en, name_fr, acronym_en, acronym_fr):
        department = Department(
            name_en=name_en,
            name_fr=name_fr,
            acronym_en=acronym_en,
            acronym_fr=acronym_fr,
        )
        department.save()
        return CreateDepartment(
            name_en=department.name_en,
            name_fr=department.name_fr,
            acronym_fr=department.acronym_fr,
            acronym_en=department.acronym_en,
        )


class CreateOrtTier(graphene.Mutation):
    name_en = graphene.String()
    name_fr = graphene.String()
    department = graphene.Field(DepartmentType)
    ownerID = graphene.Field(ProfileType)

    class Arguments:
        name_en = graphene.String()
        name_fr = graphene.String()
        department_id = graphene.Int()
        owner_gc_id = graphene.String(required=False, default_value=None)

    @staticmethod
    def mutate(self, info, name_en, name_fr, department_id, owner_gc_id=None):

        orgtier = OrgTier(
            name_en=name_en,
            name_fr=name_fr,
        )

        if owner_gc_id is None:
            orgtier.ownerID = None
        else:
            orgtier.ownerID = Profile.objects.filter(gcID=owner_gc_id).first()
            if not orgtier.ownerID:
                raise Exception('Could not find Owner ID')
        if department_id is None:
            orgtier.department = None
        else:
            orgtier.department = Department.objects.filter(id=department_id).first()
            if not orgtier.department:
                raise Exception('Could not find Department ID')

        orgtier.save()
        return CreateOrtTier(
            name_en=orgtier.name_en,
            name_fr=orgtier.name_fr,
            department=orgtier.department,
            ownerID=orgtier.department
        )


class CreateAddress(graphene.Mutation):
    street_address = graphene.String()
    city = graphene.String()
    province = graphene.String()
    postal_code = graphene.String()
    country = graphene.String(default_value="Canada")

    class Arguments:
        street_address = graphene.String()
        city = graphene.String()
        province = graphene.String()
        postal_code = graphene.String()
        country = graphene.String()

    @staticmethod
    def mutate(self, info, street_address, city, province, postal_code, country):
        address = Address(
            street_address=street_address,
            city=city,
            province=province,
            postal_code=postal_code,
            country=country,
        )
        address.save()

        return CreateAddress(
            street_address=address.street_address,
            city=address.city,
            province=address.province,
            postal_code=address.postal_code,
            country=address.country,
        )


class Query(graphene.ObjectType):
    profiles = graphene.List(ProfileType, search=graphene.String())
    addresses = graphene.List(AddressType)
    orgtiers = graphene.List(OrgTierType)
    departments = graphene.List(DepartmentType)

    @staticmethod
    def resolve_profiles(self, info, search=None, **kwargs):
        if search is not None:
    # ToDo: Add method to return a URL for avatar instead of file location
            filter = (
                Q(name__icontains=search)
            )
            return Profile.objects.filter(filter)
        return Profile.objects.all()

    @staticmethod
    def resolve_addresses(self, info, **kwargs):
        return Address.objects.all()

    @staticmethod
    def resolve_orgtiers(self, info, **kwargs):
        return OrgTier.objects.all()

    @staticmethod
    def resolve_departments(self, info, **kwargs):
        return Department.objects.all()


class Mutation(graphene.ObjectType):
    create_profile = CreateProfile.Field()
    create_department = CreateDepartment.Field()
    create_org_tier = CreateOrtTier.Field()
    create_address =CreateAddress.Field()
