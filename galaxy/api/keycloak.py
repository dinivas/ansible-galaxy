import requests
import re
import urllib
import json

__all__ = ['get_provider_token_from_keycloak']


def get_provider_token_from_keycloak(keycloakUrl, keycloakRealm, bearer_token, provider_name):
    keycloakRequestHeader = {
        'Authorization': 'Bearer ' + bearer_token}
    keyCloakIdpTokenResponse = requests.get(keycloakUrl + '/realms/' +
                                            keycloakRealm+ '/broker/' + provider_name.lower() + '/token', headers=keycloakRequestHeader)
    keyCloakIdpToken = json.loads('{"' + re.sub(r'=', r'":"', re.sub(r'&', r'","', re.sub(
        r'"/', r'\\"', urllib.parse.unquote(keyCloakIdpTokenResponse.text)))) + '"}')
    return keyCloakIdpToken
