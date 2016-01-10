# -*- coding: utf8 -*-

import default_settings
from flask.ext.plugins import Plugin
from flask import current_app as app
from pybossa.model.user import User
from sqlalchemy import event
from flask.ext.login import current_user, login_required
from gravatar import Gravatar

__plugin__ = "PyBossaGravatar"
__version__ = "0.2.0"


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
        
        @app.route('/account/set-gravatar', methods=['POST'])
        @login_required
        def set_gravatar():  # pragma: no cover
            """Set gravatar for the current user."""
            self.gravatar.set(current_user)
            