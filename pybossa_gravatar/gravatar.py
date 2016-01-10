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
        self.size = app.config['GRAVATAR_SIZE']
        self.default = app.config['GRAVATAR_DEFAULT_IMAGE']
        self.rating = app.config['GRAVATAR_SIZE']
        self.force_default = app.config['GRAVATAR_FORCE_DEFAULT']
        self.ssl = app.config['GRAVATAR_SECURE_REQUESTS']
        

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
        email_hash = hashlib.md5(email).hexdigest()
        force_default = 'y' if self.force_default else 'n'
        params = urllib.urlencode({'s': self.size, 'd': self.default,
                                   'r': self.rating, 'f': force_default})
        
        ssl = 's' if self.ssl else ''  
        base_url = u'http{0}://www.gravatar.com/avatar/{0}?{1}'
        
        return base_url.format(ssl, email_hash, params)
    
    
    def _download(self, filename, container, url):
        dl_dir = os.path.join(uploader.upload_folder, container)
        
        if not os.path.isdir(dl_dir):  # pragma: no cover
            os.makedirs(dl_dir)
        
        urllib.urlretrieve(url, os.path.join(dl_dir, filename))
