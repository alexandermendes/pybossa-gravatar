# -*- coding: utf8 -*-
"""View module for pybossa-gravatar"""

from flask import redirect, url_for, flash, abort
from flask.ext.babel import gettext
from flask.ext.login import login_required
from pybossa.core import user_repo
from pybossa.auth import ensure_authorized_to
from . import gravatar


@login_required
def set_gravatar(name): 
    """Set gravatar for a user."""
    user = user_repo.get_by(name=name)
    if not user:
        abort(404)

    ensure_authorized_to('update', user)

    gravatar.set(user)
    flash(gettext('Your avatar has been updated! It may \
                  take some minutes to refresh...'), 'success')

    return redirect(url_for('account.update_profile', name=user.name))