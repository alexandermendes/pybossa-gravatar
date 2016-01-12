# -*- coding: utf8 -*-
"""Gravatar module for pybossa-gravatar."""

import urllib
import hashlib
import os
import time
from werkzeug import secure_filename
from pybossa.cache import users as cached_users
from pybossa.core import user_repo, uploader


class GravatarClient(object):
    """Gravatar class for downloading and setting Gravatars for users.

    Parameters
    ----------
    app : obj, optional
        The Flask application.

    Attributes
    ----------
    size : int
        The size of the image.
    default : str
        The image to use if a matching Gravatar is not found.
    rating : str
        The highest acceptable image rating.
    force_default : bool
        True if the default image should always be used, False otherwise.
    ssl : bool
        True if SSL should be used, False otherwise.
    """
    
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Configure the Gravatar client."""
        self.size = app.config['GRAVATAR_SIZE']
        self.default = app.config['GRAVATAR_DEFAULT_IMAGE']
        self.rating = app.config['GRAVATAR_RATING']
        self.force_default = app.config['GRAVATAR_FORCE_DEFAULT']
        self.ssl = app.config['GRAVATAR_SECURE_REQUESTS']


    def set(self, user, update_repo=True):
        """Set a Gravatar for a user.

        Parameters
        ----------
        user : User
            The PyBossa user.
        update_repo : bool, optional
            True to save changes, False otherwise (the default is True).
        """
        url = self._get_url(user)

        now = time.time()
        filename = secure_filename('{0}_avatar.png'.format(now))
        container = 'user_{0}'.format(user.id)

        self._download(filename, container, url)

        if not user.info:  # pragma: no cover
            user.info = dict()

        user.info['avatar'] = filename
        user.info['container'] = container

        if update_repo:
            user_repo.update(user)
            cached_users.delete_user_summary(user.name)


    def _get_url(self, user):
        """Return the Gravatar URL."""
        email = hashlib.md5(user.email_addr).hexdigest()
        force_default = 'y' if self.force_default else 'n'
        params = urllib.urlencode({'s': self.size, 'd': self.default,
                                   'r': self.rating, 'f': force_default})

        base = 'https://secure' if self.ssl else 'http://www'
        
        return u'{0}.gravatar.com/avatar/{1}?{2}'.format(base, email, params)


    def _download(self, filename, container, url):
        """Download the Gravatar."""
        dl_dir = os.path.join(uploader.upload_folder, container)

        if not os.path.isdir(dl_dir):  # pragma: no cover
            os.makedirs(dl_dir)

        urllib.urlretrieve(url, os.path.join(dl_dir, filename))