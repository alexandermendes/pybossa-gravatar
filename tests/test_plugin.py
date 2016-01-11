# -*- coding: utf8 -*-

import os
import pybossa_gravatar
from mock import patch, MagicMock
from helper import web
from default import Test, with_context
from factories import UserFactory


class TestSetup(Test):
    
    
    @with_context
    def setUp(self):
        super(TestSetup, self).setUp()
        self.flask_app.config.from_object(pybossa_gravatar.default_settings)
        plugin_dir = os.path.dirname(pybossa_gravatar.__file__)
        self.plugin = pybossa_gravatar.PyBossaGravatar(plugin_dir)
        gravatar = pybossa_gravatar.Gravatar(self.flask_app)
        self.plugin.gravatar = gravatar
    
    
    @with_context
    def test_default_settings_loaded(self):
        self.plugin.load_config()
        
        assert self.flask_app.config['GRAVATAR_SIZE'] == 512
    
    
    @with_context
    def test_main_config_not_overridden_with_default_settings(self):
        self.flask_app.config['GRAVATAR_SIZE'] = 42
        self.plugin.load_config()
        
        assert self.flask_app.config['GRAVATAR_SIZE'] == 42


class TestEventListener(Test):
    
    
    @with_context
    @patch('pybossa_gravatar.gravatar.Gravatar.set', return_value=True)
    def test_event_listener_works(self, mock_set):
        user = UserFactory.create()
        
        assert mock_set.called_with(user)



class TestURLRule(web.Helper):
    
    
    @with_context
    def test_url_rule_registered(self):
        rules = [str(r) for r in self.flask_app.url_map.iter_rules()]
        
        assert '/account/<name>/update/gravatar/set' in rules
    
    
    @with_context
    def test_anon_user_cannot_set_gravatar_via_url(self,):
        res = self.app.get('/account/joebloggs/update/gravatar/set',
                            follow_redirects=True)
        
        assert "Please sign in to access this page" in res.data
        
    
    @with_context
    @patch('pybossa_gravatar.current_user', return_value=True)
    @patch('pybossa_gravatar.gravatar.Gravatar.set', return_value=True)
    def test_current_user_can_set_gravatar_via_url(self, mock_set, mock_user):
        mock_user = MagicMock()
        self.signin()
        self.app.get('/account/{0}/update/gravatar/set'.format(mock_user.name),
                      follow_redirects=True)
        
        assert mock_set.called_with(mock_user)
        

class TestGravatar(Test):
    
    
    def setUp(self):
        super(TestGravatar, self).setUp()
        self.flask_app.config.from_object(pybossa_gravatar.default_settings)
        self.gravatar = pybossa_gravatar.Gravatar(self.flask_app)
    
    
    @with_context
    @patch('pybossa_gravatar.gravatar.secure_filename', return_value='fake_fn')
    @patch('pybossa_gravatar.gravatar.Gravatar._download', return_value=True)
    def test_avatar_set_for_user(self, secure_filename, _download):
        user = UserFactory.create()
        self.gravatar.set(user, update_repo=False)
        
        assert user.info['avatar'] == 'fake_fn'
        
    
    @with_context
    @patch('pybossa_gravatar.gravatar.user_repo')
    @patch('pybossa_gravatar.gravatar.Gravatar._download', return_value=True)
    def test_repo_updated_for_user(self, _download, mock_repo):
        mock_repo = MagicMock()
        mock_repo.update.return_value = True
        user = UserFactory.create()
        self.gravatar.set(user)
        
        assert mock_repo.update.called_with(user)
    
    
    @with_context
    @patch('pybossa_gravatar.gravatar.urllib.urlretrieve', return_value=True)
    @patch('pybossa_gravatar.gravatar.uploader')
    @patch('pybossa_gravatar.gravatar.os.path.isdir', return_value=True)
    def test_url_download(self, isdir, mock_uploader, urlretrieve):
        mock_uploader = MagicMock()
        mock_uploader.upload_folder.return_value = 'upload_dir'
        self.gravatar._download('fn', 'user_1', 'http://example.com')
        path = os.path.join('upload_dir/user_1/fn')
        
        assert urlretrieve.called_with('http://example.com', path)
