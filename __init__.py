# -*- coding: utf8 -*-

from flask.ext.plugins import Plugin

__plugin__ = "PyBossaGravatar"
__version__ = "0.0.1"


class PyBossaGravatar(Plugin):
    """A PyBossa plugin for Gravatar integration."""
    
    
    def setup(self):
        """Setup plugin."""
        pass