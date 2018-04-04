import requests
from django.conf import settings
from profile.models import Profile
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


def check_token(self, info, scopes=None, **kwargs):
    authorized = True
    auth_header = info.context.META.get('HTTP_AUTHORIZATION')
    if auth_header is None:
        raise Exception('No Access token provided for protected resource')

    response = requests.get(str(settings.OIDC_USERINFO_ENDPOINT), headers={'Authorization': auth_header})

    if not response.status_code == requests.codes.ok:
        raise Exception('Invalid Access Token / Server Response ' + str(response.status_code))
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





