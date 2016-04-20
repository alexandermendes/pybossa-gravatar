# -*- coding: utf8 -*-
"""Gravatar client module for pybossa-gravatar."""

import urllib
import hashlib
import os
import time
from werkzeug import secure_filename
from pybossa.cache import users as cached_users
from pybossa.core import user_repo, uploader


class GravatarClient(object):
    """Gravatar client class.

    :param app: The pybossa application.

    :ivar size: The size of the image.
    :ivar default: The image to use if a matching Gravatar is not found.
    :ivar rating: The highest acceptable image rating.
    :ivar force_default: True to use always use default image, False otherwise.
    :ivar ssl: True if SSL should be used, False otherwise.
    """

    def __init__(self, app=None):
        self.app = app
        if app:  # pragma: no cover
            self.init_app(app)

    def init_app(self, app):
        """Configure the client."""
        self.size = app.config['GRAVATAR_SIZE']
        self.default = app.config['GRAVATAR_DEFAULT_IMAGE']
        self.rating = app.config['GRAVATAR_RATING']
        self.force_default = app.config['GRAVATAR_FORCE_DEFAULT']
        self.ssl = app.config['GRAVATAR_SECURE_REQUESTS']

    def set(self, user, update_repo=True):
        """Set a Gravatar for a user.

        :param user: The user.
        :param update_repo: True to save changes, False otherwise.
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
        """Return the Gravatar URL for a user."""
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
