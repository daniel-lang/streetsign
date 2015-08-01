'''
    First file on the noble epic tast of unit testing.
'''

import sys
import os
import tempfile
import unittest
import html5lib
from datetime import datetime
from peewee import SqliteDatabase, create_model_tables
from flask import json, url_for

sys.path.append(os.path.dirname(__file__) + '/..')

import streetsign_server
import streetsign_server.models as models
from streetsign_server.models import Post, Feed

# pylint: disable=too-many-public-methods

class WrongHTTPCode(AssertionError):
    def __init__(self, url, should_be, actually_was):
        super(WrongHTTPCode, self).__init__(
            'For Url {0}: Expected HTTP Code: {1}, actually got: {2}'
                .format(url, should_be, actually_was))

class MockBcrypt(object):
    ''' Mock BCrypt out.  It's very slow.  Which is actually good... '''

    def encrypt(self, text):
        ''' FAKE encypt a password '''
        return text

    def verify(self, text, to_compare_to):
        ''' FAKE verify a password against the hash version. '''
        return text == to_compare_to

class StreetSignTestCase(unittest.TestCase):
    ''' Base Class, initialises and tears down a streetsign_server context. '''

    def setUp(self):
        ''' initialise temporary new database. '''

        self.ctx = streetsign_server.app.test_request_context

       # streetsign_server.app.config['MODE'] = 'testing'
        models.bcrypt = MockBcrypt()
        streetsign_server.app.config['DATABASE_FILE'] = ':memory:'

        streetsign_server.app.config['TESTING'] = True

        models.DB = SqliteDatabase(None, threadlocals=True, autocommit=False)
        models.DB.init(streetsign_server.app.config['DATABASE_FILE'])

        model_list = []

        for modelname in models.__all__:
            model = getattr(models, modelname)
            try:
                model._meta.database = models.DB
                model_list.append(model)
            except AttributeError:
                pass

        create_model_tables(model_list)
        models.DB.set_autocommit(False)

        self.client = streetsign_server.app.test_client()

    def tearDown(self):
        ''' delete temporary database '''

        models.DB.close()

    def validate(self, url, lang='html', code=200, req='GET', data={}, **kwargs):
        ''' test that a URL is actually HTML5 compliant '''

        if req == 'GET':
            request = self.client.get(url, **kwargs)
        elif req=='POST':
            request = self.client.post(url, data=data, **kwargs)

        if lang == 'html':
            parser = html5lib.HTMLParser(strict=True)
            try:
                doc = parser.parse(request.data)
            except Exception as e:
                print request.data
                raise e

        elif lang == 'json':
            json.loads(request.data)


        if code != request.status_code:
            print request.data
            raise WrongHTTPCode(url, code, request.status_code)

    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password) , follow_redirects=True)
