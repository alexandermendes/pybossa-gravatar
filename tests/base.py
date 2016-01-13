# -*- coding: utf8 -*-

import os
import pybossa_gravatar as plugin
from helper import web


class PluginHelper(web.Helper):
    """Helper class for testing plugins."""
    
    
    def setUp(self):
        """Setup the plugin."""
        super(PluginHelper, self).setUp()
        with self.flask_app.app_context():
            self.flask_app.config.from_object(plugin.default_settings)
            plugin_dir = os.path.dirname(plugin.__file__)
            plugin.PyBossaGravatar(plugin_dir).setup()
            