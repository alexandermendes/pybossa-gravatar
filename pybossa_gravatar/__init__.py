# -*- coding: utf8 -*-

import default_settings
from flask import current_app as app
from flask.ext.plugins import Plugin
from .extensions import gravatar

__plugin__ = "PyBossaGravatar"
__version__ = "0.2.3"


class PyBossaGravatar(Plugin):
    """A PyBossa plugin for Gravatar integration."""


    def setup(self):
        """Setup the plugin."""
        self.load_config()
        gravatar.init_app(app)
        self.setup_url_rules()
        from . import event_listeners


    def load_config(self):
        """Configure the plugin."""
        settings = [key for key in dir(default_settings) if key.isupper()]

        for s in settings:
            if not app.config.get(s):
                app.config[s] = getattr(default_settings, s)
    
    
    def setup_url_rules(self):
        """Configure URL rules."""
        from . import view
        app.add_url_rule('/account/<name>/update/gravatar/set',
                         view_func=view.set_gravatar)
