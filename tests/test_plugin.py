# -*- coding: utf8 -*-

import os
import hashlib
import pybossa_gravatar as plugin
from mock import patch, MagicMock
from sqlalchemy import event
from pybossa.model.user import User

from factories import UserFactory
from default import Test, with_context
from .base import PluginHelper
        

class TestEventListener(Test):
    
    @with_context
    @patch('pybossa_gravatar.event_listeners.gravatar.set', return_value=True)
    def test_gravtar_set_on_add_user_event(self, mock_set):
        target = MagicMock()
        conn = MagicMock()
        plugin.event_listeners.add_user_event(None, conn, target)
        
        assert mock_set.called_with(target)
    

class TestView(PluginHelper):

    
    @with_context
    @patch('pybossa_gravatar.view.gravatar.set', return_value=True)
    def test_anon_user_redirected_to_sign_in(self, mock_set):
        self.setup_plugin()
        res = self.app.get('/account/joebloggs/update/gravatar/set',
                            follow_redirects=True)
        
        assert "Please sign in to access this page" in res.data
    
    
    @with_context
    @patch('pybossa_gravatar.view.gravatar.set', return_value=True)
    def test_unknown_user_not_found(self, mock_set):
        self.register()
        self.setup_plugin()
        res = self.app.get('/account/joebloggs/update/gravatar/set',
                            follow_redirects=True)
        
        assert res.status_code == 404
        
    
    @with_context
    @patch('pybossa_gravatar.view.ensure_authorized_to', return_value=True)
    @patch('pybossa_gravatar.view.user_repo')
    @patch('pybossa_gravatar.view.gravatar.set', return_value=True)
    def test_authorised_user_can_set_gravatar(self, mock_set, mock_repo,
                                              ensure_authorized_to):
        mock_user = MagicMock()
        mock_repo = MagicMock()
        mock_repo.return_value = mock_user
        self.register()
        self.signin()
        res = self.app.get('/account/{0}/update/gravatar/set'.format(self.name),
                            follow_redirects=True)
        
        assert mock_set.called_with(mock_user)
    
    
class TestGravatar(PluginHelper):
    
    
    def setUp(self):
        super(TestGravatar, self).setUp()
        self.flask_app.config.from_object(plugin.default_settings)
        plugin.gravatar.init_app(self.flask_app)
    
    
    @with_context
    @patch('pybossa_gravatar.gravatar_client.secure_filename',
           return_value=True)
    @patch('pybossa_gravatar.gravatar_client.user_repo')
    @patch('pybossa_gravatar.gravatar._download', return_value=True)
    def test_avatar_saved_for_user(self, _download, mock_repo, secure_filename):
        mock_repo.update.return_value = True
        user = UserFactory.create()
        plugin.gravatar.set(user)
        
        assert mock_repo.update.called_with(user)
        
    
    @with_context
    @patch('pybossa_gravatar.gravatar._download', return_value=True)
    def test_correct_url_returned(self, _download):
        plugin.gravatar.size = 42
        plugin.gravatar.rating = 'pg'
        plugin.gravatar.default = '404'
        plugin.gravatar.force_default = True
        param = 's=42&r=pg&d=404&f=y'
        
        plugin.gravatar.ssl = True
        base = 'https://secure'
        
        user = UserFactory.create()
        email = hashlib.md5(user.email_addr).hexdigest()
        
        expected = u'{0}.gravatar.com/avatar/{1}?{2}'.format(base, email, param)
        returned = plugin.gravatar._get_url(user)
        
        assert expected == returned
    
    
    @with_context
    @patch('pybossa_gravatar.gravatar_client.urllib.urlretrieve')
    @patch('pybossa_gravatar.gravatar_client.uploader')
    @patch('pybossa_gravatar.gravatar_client.os.path.isdir')
    def test_url_downloaded_to_correct_folder(self, isdir, mock_uploader,
                                              urlretrieve):
        mock_uploader = MagicMock()
        mock_uploader.upload_folder.return_value = 'upload_dir'
        urlretrieve.return_value = True
        isdir.return_value = True
        
        path = os.path.join('upload_dir/user_1/fn')
        plugin.gravatar._download('fn', 'user_1', 'http://example.com')
        
        assert urlretrieve.called_with('http://example.com', path)
