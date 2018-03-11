import requests
from django.conf import settings



def check_token(self, info, scopes):
    authorized = True
    auth_header = info.context.META.get('HTTP_AUTHORIZATION')
    if auth_header is None:
        raise Exception('No Access token provided for protected resource')

    response = requests.get(settings.OIDC_USERINFO_ENDPOINT, headers={'Authorization': auth_header}).json()
    if response is None:
        raise Exception('Invalid Access Token')

    for scope in scopes:
        if scope in response:
            authorized = authorized & True
        else:
            authorized = authorized & False

    return authorized
