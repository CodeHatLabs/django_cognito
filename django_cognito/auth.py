from importlib import import_module
import requests
from uuid import uuid4

from jose import jwt

from django.conf import settings


COGNITO_STATE = 'cognito_state'

USER_EMAIL = 'user_email'
USER_NAME = 'user_name'
USER_USERNAME = 'user_username'
USER_UUID = 'user_uuid'


class CognitoUser(object):

    def __init__(self, email, name, username, uuid):
        self.email = email
        self.name = name
        self.username = username
        self.uuid = uuid

    def is_authenticated(self):
        return True


class CognitoGuest(CognitoUser):

    def __init__(self):
        self.email = None
        self.name = 'Guest'
        self.username = None
        self.uuid = None

    def is_authenticated(self):
        return False


class BaseCognitoListener(object):

    def __init__(self, request):
        self.request = request

    def OnLogin(self):
        pass

    def OnLogout(self):
        pass


def clear_session_user(request):
    session = request.session
    if USER_EMAIL in session:
        del session[USER_EMAIL]
    if USER_NAME in session:
        del session[USER_NAME]
    if USER_USERNAME in session:
        del session[USER_USERNAME]
    if USER_UUID in session:
        del session[USER_UUID]
    _notify_cognito_listeners(request, 'OnLogout')


def _create_session_cognito_state(request):
    cognito_state = uuid4().hex
    request.session[COGNITO_STATE] = cognito_state
    return cognito_state


# method contributed by maackle@github
def _decode_jwt_payload(token):
    header = jwt.get_unverified_header(token)
    kid = header['kid']
    result = requests.get(settings.COGNITO_JWKS_URL)
    try:
        for key in result.json()['keys']:
            if key['kid'] == kid:
                claims = jwt.decode(
                    token, key,
                    algorithms=[key['alg']],
                    options={
                        'verify_aud': False,
                        'verify_at_hash': False
                    }
                )
                return claims
    except Exception:
        print("Problem getting JWK")
        raise
    return None


def _notify_cognito_listeners(request, event_name):
    for listener_entry in getattr(settings, 'COGNITO_LISTENERS', []):
        parts = listener_entry.split('.')
        module_path = '.'.join(parts[:-1])
        module = import_module(module_path)
        listener_class_name = parts[-1]
        listener_class = getattr(module, listener_class_name)
        getattr(listener_class(request), event_name)()


def set_session_user(request, claims):
    session = request.session
    session[USER_EMAIL] = claims.get('email')
    session[USER_NAME] = claims.get('name')
    session[USER_USERNAME] = claims.get('cognito:username')
    session[USER_UUID] = claims['sub']
    _notify_cognito_listeners(request, 'OnLogin')


