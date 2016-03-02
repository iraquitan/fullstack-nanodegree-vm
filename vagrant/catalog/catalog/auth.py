# -*- coding: utf-8 -*-
"""
 * Created by PyCharm.
 * Project: catalog
 * Author name: Iraquitan Cordeiro Filho
 * Author login: pma007
 * File: auth.py
 * Date: 2/25/16
 * Time: 11:46
 * To change this template use File | Settings | File Templates.
"""
import json
from flask import url_for, current_app, request, redirect, session
from rauth import OAuth2Service
import os
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
import urllib2


# Define an skeleton class to ease Oauth process
# from http://blog.miguelgrinberg.com/post/oauth-authentication-with-flask
class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('home.oauth_callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(cls, provider_name):
        if cls.providers is None:
            cls.providers = {}
            for provider_class in cls.__subclasses__():
                provider = provider_class()
                cls.providers[provider.provider_name] = provider
        return cls.providers[provider_name]


# Define Google signin
class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        super(GoogleSignIn, self).__init__('google')
        try:
            googleinfo = urllib2.urlopen(
                'https://accounts.google.com/.well-known/openid-configuration')
            google_params = json.load(googleinfo)
            self.service = OAuth2Service(
                name='google',
                client_id=self.consumer_id,
                client_secret=self.consumer_secret,
                authorize_url=google_params.get('authorization_endpoint'),
                access_token_url=google_params.get('token_endpoint'),
                base_url=google_params.get('userinfo_endpoint')
            )
        except urllib2.HTTPError:
            self.service = OAuth2Service(
                name='google',
                client_id=self.consumer_id,
                client_secret=self.consumer_secret,
                authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
                access_token_url="https://www.googleapis.com/oauth2/v4/token",
                base_url="https://www.googleapis.com/oauth2/v3/userinfo"
            )

    # Not used anymore, now authorization is started in client side
    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email profile',
            response_type='code',
            redirect_uri=self.get_callback_url())
            )

    # Google callback to get access token and retrieve user information
    def callback(self):
        auth_code = request.data
        if not auth_code:
            return None, None
        # Retrieve access token from authorization code
        oauth_session = self.service.get_auth_session(
                data={'code': auth_code,
                      'grant_type': 'authorization_code',
                      'redirect_uri': 'postmessage'
                      },
                decoder=json.loads
        )
        # Use access token to retrieve user info
        me = oauth_session.get('').json()
        user_info = (me.get('name'), me.get('email'), me.get('picture'))
        social_info = ('google', me.get('sub'), me.get('profile'))
        session['login'] = 'google'
        return (
            user_info, social_info
        )


class FacebookSignIn(OAuthSignIn):
    def __init__(self):
        super(FacebookSignIn, self).__init__('facebook')
        self.service = OAuth2Service(
            name='facebook',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://graph.facebook.com/oauth/authorize',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com/'
        )

    # Not used anymore, now authorization is started in client side
    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    # Facebook callback to get access token and retrieve user information
    def callback(self):
        auth_code = request.data
        if not auth_code:
            return None, None
        # Retrieve access token from authorization code
        oauth_session = self.service.get_auth_session(
            data={'fb_exchange_token': auth_code,
                  'grant_type': 'fb_exchange_token',
                  'redirect_uri': self.get_callback_url()}
        )
        # Use access token to retrieve user info
        me = oauth_session.get('me',
                               params={'fields': 'name,id,email,link'}).json()
        social_info = ('facebook', me.get('id'), me.get('link'))
        me_picture = oauth_session.get('me/picture',
                                       params={'redirect': 0, 'height': 400,
                                               'width': 400}).json()
        user_info = (me.get('name'), me.get('email'),
                     me_picture.get('data').get('url'))
        session['login'] = 'facebook'
        return (
            user_info, social_info
        )
