# -*- coding: utf8 -*-

import default_settings
from flask import current_app as app
from flask import redirect, url_for, flash, Blueprint, request, abort
from flask.ext.plugins import Plugin
from flask.ext.babel import gettext
from flask.ext.login import current_user, login_required
from pybossa.model.user import User
from pybossa.core import user_repo
from sqlalchemy import event
from gravatar import Gravatar

__plugin__ = "PyBossaGravatar"
__version__ = "0.2.2"


class PyBossaGravatar(Plugin):
    """A PyBossa plugin for Gravatar integration."""
    
    
    def setup(self):
        """Setup the plugin."""
        self.load_config()
        self.gravatar = Gravatar(app)
        self.setup_event_listener()
        self.setup_url_rule()
    
    
    def load_config(self):
        """Configure the plugin."""
        settings = [key for key in dir(default_settings) if key.isupper()]
        
        for s in settings:
            if not app.config.get(s):
                app.config[s] = getattr(default_settings, s)
    
    
    def setup_event_listener(self):
        """Setup event listener."""

        @event.listens_for(User, 'before_insert')
        def add_user_event(mapper, conn, target):
            """Set gravatar by default for new users."""
            self.gravatar.set(target, update_repo=False)
    
    
    def setup_url_rule(self):
        """Setup URL rule."""
        from pybossa.auth import ensure_authorized_to
        
        @app.route('/account/<name>/update/gravatar/set')
        @login_required
        def set_gravatar(name):  # pragma: no cover
            """Set gravatar for a user."""
            user = user_repo.get_by(name=name)
            if not user:
                abort(404)
            
            ensure_authorized_to('update', user)
            
            self.gravatar.set(user)
            flash(gettext('Your avatar has been updated! It may \
                          take some minutes to refresh...'), 'success')
            
            return redirect(url_for('account.update_profile', name=user.name))
            