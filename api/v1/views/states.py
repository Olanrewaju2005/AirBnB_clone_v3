#!/usr/bin/python3
"""
import important modules
"""

from flask import jsonify, abort, request
from models.state import State
from models import storage
from api.v1.views import app_views

@app_views.route('/states', strict_slashes=False)
def get_all_states():
    """
    fetches all existing states
    """
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)

@app_views.route('/states/<state_id>', strict_slashes=False)
def get_state(state_id):
    """
    retrieves a particular state using its id
    """
    state = storage.get(State, state_id)

    if state:
        return jsonify(state.to_dict())
    else:
        return abort(404)

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """
    deletes state with provided id
    """
    state = storage.get(State, state_id)

    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    creates a new state using information provided by the user
    """
    if request.content_type != 'application/json':
        return abort(404, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    kwargs = request.get_json()

    if 'name' not in kwargs:
        abort(400, 'Missing name')

    state = State(**kwargs)
    state.save()
    return jsonify(state.to_dict()), 200

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    updates information of a particular state
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    state = storage.get(State, state_id)

    if state:
        if not request.get_json():
            return abort(400, 'Not JSON')
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
    else:
        return abort(404)
