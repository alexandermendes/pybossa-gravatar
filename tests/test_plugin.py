# -*- coding: utf8 -*-

import os
import hashlib
import pybossa_gravatar
from mock import patch, MagicMock
from factories import UserFactory
from default import Test, with_context
from helper import web


class TestEventListener(Test):


    @with_context
    @patch('pybossa_gravatar.event_listeners.gravatar.set', return_value=True)
    def test_gravtar_set_on_add_user_event(self, mock_set):
        target = MagicMock()
        conn = MagicMock()
        pybossa_gravatar.event_listeners.add_user_event(None, conn, target)

        assert mock_set.called_with(target)


class TestView(web.Helper):


    @with_context
    @patch('pybossa_gravatar.view.gravatar.set', return_value=True)
    def test_anon_user_redirected_to_sign_in(self, mock_set):
        res = self.app.get('/account/joebloggs/update/gravatar/set',
                           follow_redirects=True)

        assert "Please sign in to access this page" in res.data


    @with_context
    @patch('pybossa_gravatar.view.gravatar.set', return_value=True)
    def test_unknown_user_not_found(self, mock_set):
        self.register()
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
        res = self.app.get('/account/{}/update/gravatar/set'.format(self.name),
                           follow_redirects=True)

        assert mock_set.called_with(mock_user)


class TestGravatar(Test):


    @with_context
    @patch('pybossa_gravatar.gravatar_client.secure_filename',
           return_value=True)
    @patch('pybossa_gravatar.gravatar_client.user_repo')
    @patch('pybossa_gravatar.gravatar._download', return_value=True)
    def test_avatar_saved_for_user(self, _download, mock_repo, secure_fn):
        mock_repo.update.return_value = True
        user = UserFactory.create()
        pybossa_gravatar.gravatar.set(user)

        assert mock_repo.update.called_with(user)


    @with_context
    @patch('pybossa_gravatar.gravatar._download', return_value=True)
    def test_correct_url_returned(self, _download):
        pybossa_gravatar.gravatar.size = 42
        pybossa_gravatar.gravatar.rating = 'pg'
        pybossa_gravatar.gravatar.default = '404'
        pybossa_gravatar.gravatar.force_default = True
        params = 's=42&r=pg&d=404&f=y'

        pybossa_gravatar.gravatar.ssl = True
        base = 'https://secure'

        user = UserFactory.create()
        email_hash = hashlib.md5(user.email_addr).hexdigest()

        expected = u'{0}.gravatar.com/avatar/{1}?{2}'.format(base, email_hash,
                                                             params)
        returned = pybossa_gravatar.gravatar._get_url(user)

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
        pybossa_gravatar.gravatar._download('fn', 'user_1', 'example.com')

        assert urlretrieve.called_with('example.com', path)
