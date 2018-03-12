import requests
from django.conf import settings
from profile.models import Profile
from django.db.models import Q


def check_token(self, info, scopes=None, **kwargs):
    authorized = True
    auth_header = info.context.META.get('HTTP_AUTHORIZATION')
    if auth_header is None:
        raise Exception('No Access token provided for protected resource')

    response = requests.get(settings.OIDC_USERINFO_ENDPOINT, headers={'Authorization': auth_header})
    if not response.status_code == requests.codes.ok:
        raise Exception('Invalid Access Token')
    else:
        response = response.json()

    # Check to see if the claims were authorized
    if scopes is not None:
        for scope in scopes:
            if scope in response:
                authorized = authorized & True
            else:
                authorized = authorized & False

    if 'gcID' in kwargs:
        gc_id = kwargs.get('gcID')
        if 'sub' in response and response.get('sub') == gc_id:
            authorized = authorized & True
            check_profile(response.get('sub'), response.get('name'), response.get('email'))
        else:
            authorized = authorized & False

    return authorized


def check_profile(gc_id, name, email):
    # check to see if profile exists from token 'sub' identity.  If it doesn't then create one.
    filter = (
            Q(gcID__iexact=gc_id) |
            Q(email__iexact=email)
    )
    if not Profile.objects.filter(filter).exists():
        profile = Profile(gcID=gc_id, name=name, email=email)
        profile.save()



