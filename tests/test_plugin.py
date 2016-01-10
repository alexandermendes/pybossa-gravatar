# -*- coding: utf8 -*-

import os
import pybossa_gravatar
from mock import patch, MagicMock
from helper import web
from default import Test, with_context
from factories import UserFactory
from flask.ext.login import current_user


class TestPluginSetup(Test):
    
    
    def setUp(self):
        super(TestPluginSetup, self).setUp()
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
    
    
    @with_context
    def test_set_gravatar_rule_registered(self):
        self.plugin.setup_url_rule()
        rules = [str(r) for r in self.flask_app.url_map.iter_rules()]
        
        assert '/account/set-gravatar' in rules
    
    
    @with_context
    @patch('pybossa_gravatar.gravatar.Gravatar.set', return_value=True)
    def test_event_listener_works(self, mock_set):
        self.plugin.setup_event_listener()
        user = UserFactory.create()
        
        assert mock_set.called_with(user)
    
    
    @with_context
    @patch('pybossa_gravatar.PyBossaGravatar.load_config')
    @patch('pybossa_gravatar.PyBossaGravatar.setup_event_listener')
    @patch('pybossa_gravatar.PyBossaGravatar.setup_url_rule')
    def test_all_methods_called_on_setup(self, setup_url_rule,
                                         setup_event_listener, load_config):
        load_config.return_value = True
        setup_event_listener.return_value = True
        setup_url_rule.return_value = True
        self.plugin.setup()
        
        assert load_config.called
        assert setup_event_listener.called
        assert setup_url_rule.called
        
        


class TestView(web.Helper):
    
    
    @with_context
    def test_anon_user_cannot_set_gravatar_via_url(self,):
        res = self.app.post('/account/set-gravatar', follow_redirects=True)
        
        assert "Please sign in to access this page" in res.data
        
    
    @with_context
    @patch('pybossa_gravatar.current_user', return_value=True)
    @patch('pybossa_gravatar.gravatar.Gravatar.set', return_value=True)
    def test_current_user_can_set_gravatar_via_url(self, mock_set, mock_user):
        mock_user = MagicMock()
        self.signin()
        self.app.post('/account/set-gravatar', follow_redirects=True)
        
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
