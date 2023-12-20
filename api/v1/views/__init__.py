#!/usr/bin/python3
""" Start API """

from flask import Blueprint

app.views = Blueprint('app.views', __name__, url_prefix='/api/v1')

from api.v1.views import *
