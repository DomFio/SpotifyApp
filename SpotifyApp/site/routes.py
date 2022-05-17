from flask import Blueprint, render_template
from flask_login.utils import login_required

"""
Note that in the code below,
some of the arguments are specified when creating the blueprint object
the first argument, "site", is the blueprints name
which is sed by Flasks routing mechanism

the second arg is __name__, is the blueprint import name
which flask uses to locate the blueprints resources
"""


site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')