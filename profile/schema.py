import graphene
from graphene_django import DjangoObjectType
from .models import Profile, Address, OrgTier, Organization
from django.db.models import Q
from .images import AvatarImage
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


class OrganizationType(DjangoObjectType):
    class Meta:
        model = Organization


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
            org=profile.org, )


class ModifyProfileAddressInput(graphene.InputObjectType):
    street_address = graphene.String(required=False, default_value=None)
    city = graphene.String(required=False, default_value=None)
    province = graphene.String(required=False, default_value=None)
    postal_code = graphene.String(required=False, default_value=None)
    country = graphene.String(required=False, default_value=None)


class ModifyProfileSupervisorInput(graphene.InputObjectType):
    gc_id = graphene.String(required=False, default_value=None)


class ModifyProfileOrgTierInput(graphene.InputObjectType):
    org_id = graphene.Int(required=False, default_value=None)


class ModifyProfileInput(graphene.InputObjectType):

    name = graphene.String(required=False, default_value=None)
    email = graphene.String(required=False, default_value=None)
    title_en = graphene.String(required=False, default_value=None)
    title_fr = graphene.String(required=False, default_value=None)
    mobile_phone = graphene.String(required=False, default_value=None)
    office_phone = graphene.String(required=False, default_value=None)
    address = ModifyProfileAddressInput(required=False, description='Address modifier for Profile')
    supervisor = ModifyProfileSupervisorInput(required=False, description='Supervisor modifier for Profile')
    org = ModifyProfileOrgTierInput(required=False, description='Org Tier modifier for Profile')


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
        gc_id = graphene.String(required=True, description='An individuals unique identifier as provided by the "sub"'
                                                           ' field from oidc provider in identity token')
        profile_info = ModifyProfileInput(required=True, description='A dict of values to modify. To upload an avatar'
                                                                       ' include the file in the POST request with the'
                                                                       ' name "avatar". The avatar field will not be'
                                                                       ' used and is for information only')

    @staticmethod
    def mutate(self, info, gc_id, profile_info):

        scopes = {'modify_profile'}
        kwargs = {'gcID': gc_id}

        if not Auth.auth.check_token(self, info, scopes, **kwargs):
            raise Exception('Not authorized to modify profile')

        profile = Profile.objects.get(gcID=gc_id)
        if profile is None:
            raise Exception('Could not find that profile')
        if profile_info.name is not None:
            profile.name = profile_info.name
        if profile_info.email is not None:
            profile.email = profile_info.email
        if profile_info.title_en is not None:
            profile.title_en = profile_info.title_en
        if profile_info.title_fr is not None:
            profile.title_fr = profile_info.title_fr
        if profile_info.mobile_phone is not None:
            profile.mobile_phone = profile_info.mobile_phone
        if profile_info.office_phone is not None:
            profile.office_phone = profile_info.office_phone

        if profile_info.address is not None:
            if profile.address is not None:
                if profile_info.address.street_address is not None:
                    profile.address.street_address = profile_info.address.street_address
                if profile_info.address.city is not None:
                    profile.address.city = profile_info.address.city
                if profile_info.address.province is not None:
                    profile.address.province = profile_info.address.province
                if profile_info.address.postal_code is not None:
                    profile.address.postal_code = profile_info.address.postal_code
                if profile_info.address.country is not None:
                    profile.address.country = profile_info.address.country
                profile.address.save()
            else:

                address = Address(street_address=profile_info.address.street_address,
                                          city=profile_info.address.city,
                                          province=profile_info.address.province,
                                          postal_code=profile_info.address.postal_code,
                                          country=profile_info.address.country)
                address.save()
                profile.address = address

        if profile_info.supervisor is not None:
            supervisorId = profile_info.supervisor.get('gc_id')
            if supervisorId is not None:
                supervisor = Profile.objects.get(gcID=supervisorId)
                if supervisor is not None:
                    profile.supervisor = supervisor
                else:
                    raise Exception('Could not find supervisor id')
            else:
                profile.supervisor = None

        if profile_info.org is not None:
            orgId = profile_info.org.get('org_id')
            if orgId is not None:
                org = OrgTier.objects.get(id=orgId)
                if org is not None:
                    profile.org = org
                else:
                    return Exception('Could not find Org Tier id')
            else:
                profile.org = None


        img_url = AvatarImage.setimage(self, info)
        if img_url is not None:
            profile.avatar = img_url

        profile.save()
        return profile


class DeleteProfile(graphene.Mutation):
    successful_delete = graphene.String()

    class Arguments:
        gc_id = graphene.String()

    def mutate(self, info, gc_id):
        scopes = {'modify_profile'}
        kwargs = {'gcID': gc_id}
        if not Auth.auth.check_token(self, info, scopes, **kwargs):
            raise Exception('Not Authorized to delete profile')

        profile = Profile.objects.get(gcID=gc_id)
        if profile is None:
            raise Exception('Profile does not exist')

        else:
            address = Address.objects.get(id=profile.address.id)
            address.delete()
            profile.delete()
            return DeleteProfile(successful_delete="True")


class CreateOrganization(graphene.Mutation):
    id = graphene.Int()
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
        if Organization.objects.filter(filter).exists():
            raise Exception('Organization with that information already exists')

        organization = Organization(
            name_en=name_en,
            name_fr=name_fr,
            acronym_en=acronym_en,
            acronym_fr=acronym_fr,
        )
        organization.save()
        return CreateOrganization(
            id=organization.id,
            name_en=organization.name_en,
            name_fr=organization.name_fr,
            acronym_fr=organization.acronym_fr,
            acronym_en=organization.acronym_en,
        )


class ModifyOrganizationInput(graphene.InputObjectType):
    name_en = graphene.String(required=False, default=None)
    name_fr = graphene.String(required=False, default=None)
    acronym_fr = graphene.String(required=False, default=None)
    acronym_en = graphene.String(required=False, default=None)


class ModifyOrganization(graphene.Mutation):
    id = graphene.Int()
    name_en = graphene.String()
    name_fr = graphene.String()
    acronym_fr = graphene.String()
    acronym_en = graphene.String()

    class Arguments:
        organization_id = graphene.Int()
        data_to_modify = ModifyOrganizationInput(required=True)

    @staticmethod
    def mutate(self, info, organization_id, data_to_modify):
        organization = Organization.objects.get(id=organization_id)
        if organization is None:
            raise Exception('Organization ID does not exist')
        if data_to_modify.name_en is not None:
            organization.name_en = data_to_modify.name_en
        if data_to_modify.name_fr is not None:
            organization.name_fr = data_to_modify.name_fr
        if data_to_modify.acronym_en is not None:
            organization.acronym_en = data_to_modify.acronym_en
        if data_to_modify.acronym_fr is not None:
            organization.acronym_fr = data_to_modify.acronym_fr

        organization.save()

        return organization


class DeleteOrganization(graphene.Mutation):
    successful_delete = graphene.String()

    class Arguments:
        organization_id = graphene.Int()

    def mutate(self, info, organization_id):
        organization = Organization.objects.get(id=organization_id)
        if organization is None:
            raise Exception('organization ID does not exist')

        organization.delete()
        return DeleteOrganization(successful_delete='True')


class CreateOrgTier(graphene.Mutation):
    id = graphene.Int()
    name_en = graphene.String()
    name_fr = graphene.String()
    organization = graphene.Field(OrganizationType)
    ownerID = graphene.Field(ProfileType)

    class Arguments:
        name_en = graphene.String()
        name_fr = graphene.String()
        organization_id = graphene.Int()
        owner_gc_id = graphene.String(required=False, default_value=None)

    @staticmethod
    def mutate(self, info, name_en, name_fr, organization_id, owner_gc_id=None):

        filter = (
            Q(name_en__iexact=name_en) &
            Q(name_fr__iexact=name_fr) &
            Q(organization__id__exact=organization_id)
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
        if organization_id is None:
            orgtier.organization = None
        else:
            orgtier.organization = Organization.objects.filter(id=organization_id).first()
            if not orgtier.organization:
                raise Exception('Could not find Organization ID')

        orgtier.save()
        return CreateOrgTier(
            orgId=orgtier.id,
            name_en=orgtier.name_en,
            name_fr=orgtier.name_fr,
            organization=orgtier.organization,
            ownerID=orgtier.organization
        )


class ModifyOrgTierInput(graphene.InputObjectType):
    name_en = graphene.String(required=False, default_value=None)
    name_fr = graphene.String(required=False, default_value=None)
    organization_id = graphene.Int(required=False, default_value=None)
    owner_gc_id = graphene.String(required=False, default_value=None)


class ModifyOrgTier(graphene.Mutation):
    id = graphene.Int()
    name_en = graphene.String()
    name_fr = graphene.String()
    organization = graphene.Field(OrganizationType)
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
        if data_to_modify.organization_id is not None:
            organization = Organization.objects.get(id=data_to_modify.organization_id)
            if organization is not None:
                org.organization = organization

            else:
                raise Exception('Could not find Organization ID')
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


class ProfileQuery(graphene.ObjectType):
    profiles = graphene.List(ProfileType, gcID=graphene.String(), name=graphene.String(), email=graphene.String(),
                             mobile_phone=graphene.String(), office_phone=graphene.String(),
                             title_en=graphene.String(), title_fr=graphene.String(), first=graphene.Int(),
                             skip=graphene.Int())
    addresses = graphene.List(AddressType, street_address=graphene.String(), city=graphene.String(), province=graphene.String(),
                              postal_code=graphene.String(), country=graphene.String(), first=graphene.Int(), skip=graphene.Int())
    orgtiers = graphene.List(OrgTierType, name_en=graphene.String(), name_fr=graphene.String(), first=graphene.Int(),
                             skip=graphene.Int())
    organizations = graphene.List(OrganizationType, name_en=graphene.String(), name_fr=graphene.String(),
                                  acronym_en=graphene.String(), acronym_fr=graphene.String(), first=graphene.Int(),
                                  skip=graphene.Int())

    @staticmethod
    # ToDo: Add method to return a URL for avatar instead of file location
    def resolve_profiles(self, info, **kwargs):

        if kwargs is not None:
            filter = Q()
            if 'gcID' in kwargs:
                return Profile.objects.filter(gcID=kwargs.get('gcID'))
            if 'name' in kwargs:
                filter.add(Q(name__icontains=kwargs.get('name')), Q.AND)
            if 'email' in kwargs:
                filter.add(Q(email__iexact=kwargs.get('email')), Q.AND)
            if 'mobile_phone' in kwargs:
                filter.add(Q(mobile_phone__icontains=kwargs.get('mobile_phone')), Q.AND)
            if 'office_phone' in kwargs:
                filter.add(Q(office_phone__icontains=kwargs.get('office_phone')), Q.AND)
            if 'title_en' in kwargs:
                filter.add(Q(title_en__icontains=kwargs.get('title_en')), Q.AND)
            if 'title_fr' in kwargs:
                filter.add(Q(title_fr__icontains=kwargs.get('title_fr')), Q.AND)

            qs = Profile.objects.filter(filter)

            if 'skip' in kwargs:
                qs = qs[kwargs.get('skip')::]
            if 'first' in kwargs:
                qs = qs[:kwargs.get('first')]

            return qs

        return Profile.objects.all()

    @staticmethod
    def resolve_addresses(self, info, **kwargs):
        if kwargs is not None:
            filter = Q()
            if 'id' in kwargs:
                return Address.objects.filter(id=kwargs.get('id'))
            if 'street_address' in kwargs:
                filter.add(Q(street_address__icontains=kwargs.get('street_address')), Q.AND)
            if 'city' in kwargs:
                filter.add(Q(city__icontains=kwargs.get('city')), Q.AND)
            if 'province' in kwargs:
                filter.add(Q(province__iexact=kwargs.get('province')), Q.AND)
            if 'postal_code' in kwargs:
                filter.add(Q(postal_code__iexact=kwargs.get('postal_code')), Q.AND)
            if 'country' in kwargs:
                filter.add(Q(country__iexact=kwargs.get('country')), Q.AND)

            qs = Address.objects.filter(filter)

            if 'skip' in kwargs:
                qs = qs[kwargs.get('skip')::]
            if 'first' in kwargs:
                qs = qs[:kwargs.get('first')]

            return qs

        return Address.objects.all()

    @staticmethod
    def resolve_orgtiers(self, info, **kwargs):
        if kwargs is not None:
            filter = Q()
            if 'id' in kwargs:
                return OrgTier.objects.filter(id=kwargs.get('id'))
            if 'name_en' in kwargs:
                filter.add(Q(name_en__icontains=kwargs.get('name_en')), Q.AND)
            if 'name_fr' in kwargs:
                filter.add(Q(name_fr__icontains=kwargs.get('name_fr')), Q.AND)

            qs = OrgTier.objects.filter(filter)

            if 'skip' in kwargs:
                qs = qs[kwargs.get('skip')::]
            if 'first' in kwargs:
                qs = qs[:kwargs.get('first')]

            return qs

        return OrgTier.objects.all()

    @staticmethod
    def resolve_organizations(self, info, **kwargs):
        if kwargs is not None:
            filter = Q()
            if 'id' in kwargs:
                return Organization.objects.filter(id=kwargs.get('id'))
            if 'name_en' in kwargs:
                filter.add(Q(name_en__icontains=kwargs.get('name_en')), Q.AND)
            if 'name_fr' in kwargs:
                filter.add(Q(name_fr__icontains=kwargs.get('name_en')), Q.AND)
            if 'acronym_en' in kwargs:
                filter.add(Q(acronym_en__iexact=kwargs.get('acronym_en')), Q.AND)
            if 'acronym_fr' in kwargs:
                filter.add(Q(acronym_fr__iexact=kwargs.get('acronym_fr')), Q.AND)

            qs = Organization.objects.filter(filter)

            if 'skip' in kwargs:
                qs = qs[kwargs.get('skip')::]
            if 'first' in kwargs:
                qs = qs[:kwargs.get('first')]

            return qs

        return Organization.objects.all()


class ProfileMutation(graphene.ObjectType):

    modify_profile = ModifyProfile.Field()
    create_org_tier = CreateOrgTier.Field()
    modify_org_tier = ModifyOrgTier.Field()
    delete_org_tier = DeleteOrgTier.Field()


class ProtectedProfileMutation(graphene.ObjectType):
    delete_profile = DeleteProfile.Field()
    modify_profile = ModifyProfile.Field()
    create_profile = CreateProfile.Field()
    create_organization = CreateOrganization.Field()
    delete_organization = DeleteOrganization.Field()
    modify_organization = ModifyOrganization.Field()
    create_org_tier = CreateOrgTier.Field()
    modify_org_tier = ModifyOrgTier.Field()
    delete_org_tier = DeleteOrgTier.Field()


class ProtectedMutation(ProtectedProfileMutation, graphene.ObjectType):
    pass


class ProtectedQuery(ProfileQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=ProtectedQuery, mutation=ProtectedMutation)
