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
        else:
            authorized = authorized & False

    return authorized





