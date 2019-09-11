#!/usr/bin/python3
'''creates new view for State objects and handels all default RESTAPI actions'''
from flask import Flask, request
from api.v1.views import app_views
from models import storage
from models.state import State

@app_views.route('/states', strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state():
    '''retrieves state object'''
    ids = 'state_id'
    state = get('State', ids) 
    if state:
        return state
    else:
        return stats()
