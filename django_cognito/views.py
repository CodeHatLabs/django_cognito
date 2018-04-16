from base64 import b64decode
import json
import requests

from django.conf import settings
from django.http import HttpResponseRedirect

from .auth import (
    clear_session_user,
    _create_session_cognito_state,
    COGNITO_STATE,
    _decode_jwt_payload,
    set_session_user
    )


def login(request):
    cognito_login_uri = settings.COGNITO_LOGIN_URI_TEMPLATE \
                                % _create_session_cognito_state(request)
    return HttpResponseRedirect(cognito_login_uri)


def login_callback(request):
    session = request.session
    state = request.GET.get('state')
    if (not state) or (state != session.get(COGNITO_STATE)):
        print(
            """login_callback fail: (not state) or (%s != "%s")"""
                % (state, session.get(COGNITO_STATE)))
        return login(request)
    code = request.GET.get('code')
    result = requests.post(
        settings.COGNITO_API_TOKEN_URI,
        headers = settings.COGNITO_API_TOKEN_HEADERS,
        data = {
            'grant_type': 'authorization_code',
            'client_id': settings.COGNITO_CLIENT_ID,
            'code': code,
            'redirect_uri': settings.COGNITO_REDIRECT_LOGIN_URI
            }
        )
    if result.status_code != 200:
        print("""login_callback fail: %s != 200""" % result.status_code)
        return login(request)
    try:
        token = result.json()['id_token']
        claims = _decode_jwt_payload(token)
    except Exception as ex:
        print("""login_callback fail: %s""" % ex)
        return login(request)
    if COGNITO_STATE in session:
        del session[COGNITO_STATE]
    set_session_user(session, claims)
    return HttpResponseRedirect(settings.COGNITO_LOGIN_SUCCESS_REDIRECT)


def logout(request):
    clear_session_user(request.session)
    return HttpResponseRedirect(settings.COGNITO_LOGOUT_URI)


def logout_callback(request):
    return HttpResponseRedirect(settings.COGNITO_LOGOUT_SUCCESS_REDIRECT)


