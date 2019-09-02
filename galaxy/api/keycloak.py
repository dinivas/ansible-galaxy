import requests
import re
import urllib
import json

__all__ = ['get_provider_token_from_keycloak']


def get_provider_token_from_keycloak(request, provider_name):
    keycloakUrl = request.realm.realm_api_client.server_url
    keycloakRequestHeader = {
        'Authorization': 'Bearer ' + request.META.get('HTTP_AUTHORIZATION').split()[1]}
    keyCloakIdpTokenResponse = requests.get(keycloakUrl + '/realms/' +
                                            request.realm.name + '/broker/' + provider_name.lower() + '/token', headers=keycloakRequestHeader)
    keyCloakIdpToken = json.loads('{"' + re.sub(r'=', r'":"', re.sub(r'&', r'","', re.sub(
        r'"/', r'\\"', urllib.parse.unquote(keyCloakIdpTokenResponse.text)))) + '"}')
    return keyCloakIdpToken
