import json
import os
import requests

from requests_oauthlib import OAuth2Session


def main():
    constants = json.load(open(os.path.join(os.path.dirname(__file__), "constants.json")))

    session = requests.Session()
    # arrange variables
    username = constants['USERNAME']
    password = constants['PASSWORD']
    client_id = '0b72c581-2e98-4644-989c-52c76e34842b'
    authorization_base_url = 'https://uam1.dexcom.com/identity/connect/authorize'
    redirect_uri = 'https://uam1.dexcom.com/auth.html'
    scope = 'AccountManagement'

    # get authorization token
    dexcom = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    authorization_url, state = dexcom.authorization_url(authorization_base_url)
    request_body = {
        'username': username,
        'password': password,
        'grant_type': 'authorization_code',
        'code': 'token',
        'redirect_uri': redirect_uri
    }
    authorization_url = authorization_url.replace('code', 'token')
    get_oauth_token = session.post('https://uam1.dexcom.com/identity/login?signin', data=request_body)
    get_bearer_token = session.post(authorization_url)
    oauth_token = session.cookies['idsrv.xsrf']

    # I am unable to figure out how to get the Bearer token from the authorization server. From what I've read about
    # OAuth2 authentication, a request must be sent to the oauth endpoint in order to receive an access token (in this
    # case, it appears to be stored in the idsrv.xsrf cookie), then that  token can be used to send to an authorization
    # endpoint, which will return a Bearer token. However, looking at the Network tab in the browser, no such token is
    # returned by the auth endpoint. I can SEE the Bearer JWT token in the Location header of the response, but there
    # would be no good way to retrieve it from there, and that's probably not how it is supposed to be done.

    # send request to api
    bearer_token = ''
    api_response = requests.post('https://myaccount.dexcom.com/api/subject/1594950620847472640/analysis_session',
                                 headers={'Authorization': 'Bearer ' + bearer_token})
    assert api_response.get('analysisSessionId') is not None


main()
