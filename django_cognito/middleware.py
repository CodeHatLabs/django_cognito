from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from .auth import *


class AuthenticationMiddleware(MiddlewareMixin):

    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The django_cognito authentication middleware requires session "
            "middleware to be installed. Edit your MIDDLEWARE setting to "
            "insert 'django.contrib.sessions.middleware.SessionMiddleware' "
            "before 'django_cognito.middleware.AuthenticationMiddleware'."
            )
        session = request.session
        request.cognito_user = SimpleLazyObject(
            lambda: CognitoUser(
                email = session[USER_EMAIL],
                name = session[USER_NAME],
                username = session[USER_USERNAME],
                uuid = session[USER_UUID]
                ) if USER_UUID in session else CognitoGuest()
            )


