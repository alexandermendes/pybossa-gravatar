# -*- coding: utf8 -*-
"""Main module for pybossa-gravatar."""

import urllib
import hashlib
import os
import time
from werkzeug import secure_filename
from pybossa.cache import users as cached_users
from pybossa.core import user_repo, uploader
from pybossa.model.user import User


class Gravatar(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
            
    
    def init_app(self, app):
        self.default = app.config['GRAVATAR_DEFAULT']
        self.size = app.config['GRAVATAR_SIZE']
        

    def set(self, user, update_repo=True):
        """Set a gravatar for a user."""
        url = self._get_url(user)
        
        now = time.time()
        filename = secure_filename('{0}_gravatar.png'.format(now))
        container = 'user_{0}'.format(user.id)
        
        self._download(filename, container, url)
        
        user.info['avatar'] = filename
        user.info['container'] = container
        
        if update_repo:
            user_repo.update(user)
            cached_users.delete_user_summary(user.name)
    
    
    def _get_url(self, user):
        """Return the gravatar URL."""
        email = user.email_addr.lower()
        e_hash = hashlib.md5(email).hexdigest()
        params = urllib.urlencode({'d': self.default, 's': self.size})
        return 'http://www.gravatar.com/avatar/{0}?{1}'.format(e_hash, params)
    
    
    def _download(self, filename, container, url):
        dl_dir = os.path.join(uploader.upload_folder, container)
        
        if not os.path.isdir(dl_dir):  # pragma: no cover
            os.makedirs(dl_dir)
        
        urllib.urlretrieve(url, os.path.join(dl_dir, filename))
