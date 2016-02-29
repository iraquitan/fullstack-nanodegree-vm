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
import os

# os.environ['http_proxy'] = ''
# os.environ['https_proxy'] = ''
# os.environ['HTTP_PROXY'] = ''
# os.environ['HTTPS_PROXY'] = ''
import urllib2

from flask import url_for, current_app, request, redirect
from rauth import OAuth2Service


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


class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        super(GoogleSignIn, self).__init__('google')
        # googleinfo = urllib2.urlopen(
        #     'https://accounts.google.com/.well-known/openid-configuration')
        # google_params = json.load(googleinfo)
        self.service = OAuth2Service(
                name='google',
                client_id=self.consumer_id,
                client_secret=self.consumer_secret,
                authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
                # authorize_url=google_params.get('authorization_endpoint'),
                access_token_url="https://www.googleapis.com/oauth2/v4/token",
                # access_token_url=google_params.get('token_endpoint'),
                base_url="https://www.googleapis.com/oauth2/v3/userinfo"
                # base_url=google_params.get('userinfo_endpoint')
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email profile',
            response_type='code',
            redirect_uri=self.get_callback_url())
            )

    def callback(self):
        auth_code = request.data
        # if 'code' not in request.args:
        if not auth_code:
            # return None, None, None, None
            return None, None
        oauth_session = self.service.get_auth_session(
                data={'code': auth_code,
                      'grant_type': 'authorization_code',
                      'redirect_uri': 'postmessage'
                      },
                decoder=json.loads
        )
        me = oauth_session.get('').json()
        user_info = (me.get('name'), me.get('email'), me.get('picture'))
        social_info = ('google', me.get('sub'),
                       oauth_session.access_token, me.get('profile'))
        return (
            user_info, social_info
        )
        # return (
        #     "google${}".format(me['sub']),
        #     me['name'],
        #     me['email'],
        #     me['picture']
        # )


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

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        auth_code = request.data
        # if 'code' not in request.args:
        if not auth_code:
            # return None, None, None, None
            return None, None
        oauth_session = self.service.get_auth_session(
            data={'fb_exchange_token': auth_code,
                  'grant_type': 'fb_exchange_token',
                  'redirect_uri': self.get_callback_url()}
            # data={'code': auth_code,
            #       'grant_type': 'authorization_code',
            #       'redirect_uri': self.get_callback_url()}
        )
        me = oauth_session.get('me',
                               params={'fields': 'name,id,email,link'}).json()
        social_info = ('facebook', me.get('id'), oauth_session.access_token,
                  me.get('link'))
        me_picture = oauth_session.get('me/picture',
                                       params={'redirect': 0, 'height': 200,
                                               'width': 200}).json()
        user_info = (me.get('name'), me.get('email'),
                me_picture.get('data').get('url'))
        return (
            user_info, social_info
        )
        # return (
        #     "facebook${}".format(me['id']),
        #     me.get('name'),
        #     me.get('email'),
        #     me_picture.get('data')['url']
        # )
