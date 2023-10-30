#!/usr/bin/python3
"""This module defines a Blueprint for the API, which includes various routes
and views for the API version 1. The Blueprint is configured with a URL
prefix of '/api/v1'.
"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.places_amenities import *
from api.v1.views.users import *
from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.places_reviews import *
from api.v1.views.places import *
from api.v1.views.states import *

