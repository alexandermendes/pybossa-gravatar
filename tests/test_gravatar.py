# -*- coding: utf8 -*-

import os
from mock import patch, MagicMock
from default import Test, with_context
from factories import UserFactory
from pybossa_gravatar.gravatar import Gravatar


class TestGravatar(Test):
    
    def setUp(self):
        super(TestGravatar, self).setUp()
        self.gravatar = Gravatar(self.flask_app)
    
    
    @patch('pybossa_gravatar.gravatar.time.time', return_value='fake_time')
    def test_default_avatar_automatically_set_for_new_user(self, time):
        user = UserFactory.create()
        
        assert user.info['avatar'].startswith('fake_time')
    
    
    @patch('pybossa_gravatar.gravatar.urllib.urlretrieve', return_value=True)
    def test_gravatar_set_for_user(self, urlretrieve):
        user = UserFactory.create()
        user.info.pop('avatar', None)
        self.gravatar.set(user)
        
        assert user.info.get('avatar')