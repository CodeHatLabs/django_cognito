from django.utils.functional import SimpleLazyObject

from django_cognito.auth import *


class AuthenticationMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        session = request.session
        request.cognito_user = SimpleLazyObject(
            lambda: CognitoUser(
                email = session[USER_EMAIL],
                name = session[USER_NAME],
                username = session[USER_USERNAME],
                uuid = session[USER_UUID]
                ) if USER_UUID in session else CognitoGuest()
            )
        return self.get_response(request)


