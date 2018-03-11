import graphene
from graphene_django import DjangoObjectType
from .models import Profile, Address, OrgTier, Department
from django.db.models import Q
import Auth.auth


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


class ModifyProfileInput(graphene.InputObjectType):

    name = graphene.String(required=False, default_value=None)
    email = graphene.String(required=False, default_value=None)
    title_en = graphene.String(required=False, default_value=None)
    title_fr = graphene.String(required=False, default_value=None)
    avatar = graphene.String(required=False, default_value=None)
    mobile_phone = graphene.String(required=False, default_value=None)
    office_phone = graphene.String(required=False, default_value=None)
    address_id = graphene.Int(required=False, default_value=None)
    supervisor_gc_id = graphene.String(required=False, default_value=None)
    org_id = graphene.Int(required=False, default_value=None)


class ModifyProfile(graphene.Mutation):
    # ToDo: Change avatar type to a file upload instead of a url/file string
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
        gc_id = graphene.String(description='An individuals unique identifier as provided by the "sub" field from oidc'
                                            ' provider in identity token')
        data_to_modify = ModifyProfileInput(required=True, description='A dict of values to modify')

    @staticmethod
    def mutate(self, info, gc_id, data_to_modify):

        scopes = {'modify_profile'}
        kwargs = {'gcID': gc_id}

        if not Auth.auth.check_token(self, info, scopes, **kwargs):
            raise Exception('Not authorized to modify profile')

        profile = Profile.objects.get(gcID=gc_id)
        if profile is None:
            raise Exception('Could not find that profile')
        if data_to_modify.name is not None:
            profile.name = data_to_modify.name
        if data_to_modify.email is not None:
            profile.email = data_to_modify.email
        if data_to_modify.title_en is not None:
            profile.title_en = data_to_modify.title_en
        if data_to_modify.title_fr is not None:
            profile.title_fr = data_to_modify.title_fr
        if data_to_modify.avatar is not None:
            profile.avatar = data_to_modify.avatar
        if data_to_modify.mobile_phone is not None:
            profile.mobile_phone = data_to_modify.mobile_phone
        if data_to_modify.office_phone is not None:
            profile.office_phone = data_to_modify.office_phone
        if data_to_modify.address_id is not None:
            address = Address.objects.get(id=data_to_modify.address_id)
            if address is not None:
                profile.address = address
            else:
                raise Exception('Could not find address with that id')
        if data_to_modify.supervisor_gc_id is not None:
            supervisor = Profile.objects.get(gcID=data_to_modify.supervisor_gc_id)
            if supervisor is not None:
                profile.supervisor = supervisor
            else:
                raise Exception('Could not find supervisor id')
        if data_to_modify.org_id is not None:
            org = OrgTier.objects.get(id=data_to_modify.org_id)
            if org is not None:
                profile.org = org
            else:
                return Exception('Could not fin Org Tier id')

        profile.save()
        return profile


class CreateProfile(graphene.Mutation):
    # ToDo: Change avatar type to a file upload instead of a url/file string
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
    def mutate(self, info, gc_id, name, email, optional_data=None):

        filter = (
            Q(gcID__iexact=gc_id) |
            Q(email__iexact=email)
        )
        if Profile.objects.filter(filter).exists():
            raise Exception('Profile with same unique keys (gcID or email) already exists')

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
                    raise Exception('Address ID does not exist')
            if optional_data.supervisor_gc_id is None:
                profile.supervisor = None
            else:
                profile.supervisor = Profile.objects.filter(gcID=optional_data.supervisor_gc_id).first()
                if not profile.supervisor:
                    raise Exception('Supervisor gcID does not exist')
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


class DeleteProfile(graphene.Mutation):
    successful_delete = graphene.String()

    class Arguments:
        gc_id = graphene.String()

    def mutate(self, info, gc_id):
        profile = Profile.objects.get(gcID=gc_id)
        if profile is None:
            raise Exception('Profile does not exist')

        else:
            profile.delete()
            return DeleteProfile(successful_delete="True")


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

        filter = (
            Q(name_en__iexact=name_en) &
            Q(name_fr__iexact=name_fr) &
            Q(acronym_en__iexact=acronym_en) &
            Q(acronym_fr__iexact=acronym_fr)
        )
        if Department.objects.filter(filter).exists():
            raise Exception('Department with that information already exists')

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


class ModifyDepartmentInput(graphene.InputObjectType):
    name_en = graphene.String(required=False, default=None)
    name_fr = graphene.String(required=False, default=None)
    acronym_fr = graphene.String(required=False, default=None)
    acronym_en = graphene.String(required=False, default=None)


class ModifyDepartment(graphene.Mutation):
    name_en = graphene.String()
    name_fr = graphene.String()
    acronym_fr = graphene.String()
    acronym_en = graphene.String()

    class Arguments:
        deptartment_id = graphene.Int()
        data_to_modify = ModifyDepartmentInput(required=True)

    @staticmethod
    def mutate(self, info, department_id, data_to_modify):
        dept = Department.objects.get(id=department_id)
        if dept is None:
            raise Exception('Department ID does not exist')
        if data_to_modify.name_en is not None:
            dept.name_en = data_to_modify.name_en
        if data_to_modify.name_fr is not None:
            dept.name_fr = data_to_modify.name_fr
        if data_to_modify.acronym_en is not None:
            dept.acronym_en = data_to_modify.acronym_en
        if data_to_modify.acronym_fr is not None:
            dept.acronym_fr = data_to_modify.acronym_fr

        dept.save()

        return dept


class DeleteDepartment(graphene.Mutation):
    successful_delete = graphene.String()

    class Arguments:
        department_id = graphene.Int()

    def mutate(self, info, department_id):
        department = Department.objects.get(id=department_id)
        if department is None:
            raise Exception('Department ID does not exist')

        department.delete()
        return DeleteDepartment(successful_delete='True')


class CreateOrgTier(graphene.Mutation):
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

        filter = (
            Q(name_en__iexact=name_en) &
            Q(name_fr__iexact=name_fr) &
            Q(department__id__exact=department_id)
        )

        if OrgTier.objects.filter(filter).exists():
            raise Exception('Org Tier with that information already exists')

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
        return CreateOrgTier(
            name_en=orgtier.name_en,
            name_fr=orgtier.name_fr,
            department=orgtier.department,
            ownerID=orgtier.department
        )


class ModifyOrgTierInput(graphene.InputObjectType):
    name_en = graphene.String(required=False, default_value=None)
    name_fr = graphene.String(required=False, default_value=None)
    department_id = graphene.Int(required=False, default_value=None)
    owner_gc_id = graphene.String(required=False, default_value=None)


class ModifyOrgTier(graphene.Mutation):
    name_en = graphene.String()
    name_fr = graphene.String()
    department = graphene.Field(DepartmentType)
    ownerID = graphene.Field(ProfileType)

    class Arguments:
        org_id = graphene.Int()
        data_to_modify = ModifyOrgTierInput(required=True)

    @staticmethod
    def mutate(self, info, org_id, data_to_modify):
        org = OrgTier.objects.get(id=org_id)
        if org is None:
            raise Exception('Could not find Org Tier ID')
        if data_to_modify.name_en is not None:
            org.name_en = data_to_modify.name_en
        if data_to_modify.name_fr is not None:
            org.name_fr = data_to_modify.name_fr
        if data_to_modify.department_id is not None:
            dept = Department.objects.get(id=data_to_modify.department_id)
            if dept is not None:
                org.department = dept

            else:
                raise Exception('Could not find Department ID')
        if data_to_modify.owner_gc_id is not None:
            profile = Profile.objects.get(gcID=data_to_modify.owner_gc_id)
        if profile is None:
            raise Exception('Could not find Org Owner ID')
        else:
            org.ownerID = profile

        org.save()

        return org


class DeleteOrgTier(graphene.Mutation):
    successful_delete = graphene.String()

    class Arguments:
        org_tier_id = graphene.Int()

    def mutate(self, info, org_tier_id):
        org = OrgTier.objects.get(id=org_tier_id)
        if org is None:
            raise Exception('Org Tier ID does not exist')

        org.delete()

        return DeleteOrgTier(successful_delete='True')


class ModifyAddressInput(graphene.InputObjectType):
    street_address = graphene.String(required=False, default_value=None)
    city = graphene.String(required=False, default_value=None)
    province = graphene.String(required=False, default_value=None)
    postal_code = graphene.String(required=False, default_value=None)
    country = graphene.String(required=False, default_value=None)


class ModifyAddress(graphene.Mutation):
    street_address = graphene.String()
    city = graphene.String()
    province = graphene.String()
    postal_code = graphene.String()
    country = graphene.String()

    class Arguments:
        address_id = graphene.Int()
        data_to_modify = ModifyAddressInput(required=True)

    @staticmethod
    def mutate(self, info, address_id, data_to_modify):
        address = Address.objects.get(id=address_id)
        if address is None:
            raise Exception('Could not find Address ID')
        if data_to_modify.street_address is not None:
            address.street_address = data_to_modify.street_address
        if data_to_modify.city is not None:
            address.city = data_to_modify.city
        if data_to_modify.province is not None:
            address.province = data_to_modify.province
        if data_to_modify.postal_code is not None:
            address.postal_code = data_to_modify.postal_code
        if data_to_modify.country is not None:
            address.country = data_to_modify.country

        address.save()

        return address


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

        filter = (
            Q(street_address__iexact=street_address) &
            Q(city__iexact=city) &
            Q(province__iexact=province) &
            Q(postal_code__iexact=postal_code) &
            Q(country__iexact=country)
        )

        if Address.objects.filter(filter).exists():
            raise Exception('Address with that information already exists')

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


class DeleteAddress(graphene.Mutation):
    successful_delete = graphene.String()

    class Arguments:
        address_id = graphene.Int()

    def mutate(self, info, address_id):
        address = Address.objects.get(id=address_id)
        if address is None:
            raise Exception('Address ID does not exist')

        address.delete()

        return DeleteAddress(successful_delete='True')


class Query(graphene.ObjectType):
    profiles = graphene.List(ProfileType, search_name=graphene.String(), gcID=graphene.String())
    addresses = graphene.List(AddressType)
    orgtiers = graphene.List(OrgTierType)
    departments = graphene.List(DepartmentType)

    @staticmethod
    # ToDo: Add method to return a URL for avatar instead of file location
    def resolve_profiles(self, info, search_name=None, gcID=None, **kwargs):
        if search_name is not None:
            filter = (
                Q(name__icontains=search_name)
            )
            return Profile.objects.filter(filter)

        if gcID is not None:
            return Profile.objects.filter(gcID=gcID)

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


class ProfileMutation(graphene.ObjectType):
    create_profile = CreateProfile.Field()
    create_department = CreateDepartment.Field()
    create_org_tier = CreateOrgTier.Field()
    create_address = CreateAddress.Field()
    modify_profile = ModifyProfile.Field()
    modify_department = ModifyDepartment.Field()
    modify_org_tier = ModifyOrgTier.Field()
    modify_address = ModifyAddress.Field()
    delete_profile = DeleteProfile.Field()
    delete_department = DeleteDepartment.Field()
    delete_org = DeleteOrgTier.Field()
    delete_address = DeleteAddress.Field()




