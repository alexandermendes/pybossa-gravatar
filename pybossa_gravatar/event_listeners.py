# -*- coding: utf8 -*-
"""Event listeners module for pybossa-gravatar."""

from pybossa.model.user import User
from sqlalchemy import event
from . import gravatar


@event.listens_for(User, 'before_insert')
def add_user_event(mapper, conn, target):
    """Set Gravatar by default for new users."""
    gravatar.set(target, update_repo=False)
