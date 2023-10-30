#!/usr/bin/python3
'''
    RESTful API for class State
'''
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@swag_from('docs/state/get_state.yml', methods=['GET'])
def get_state():
    '''
        return state in json form
    '''
    state_list = [s.to_dict() for s in storage.all('State').values()]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
@swag_from('docs/state/get_state_id.yml', methods=['GET'])
def get_state_id(state_id):
    '''
        return state and its id using http verb GET
    '''
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route(
    '/states/<state_id>',
    methods=['DELETE'],
    strict_slashes=False)
@swag_from('docs/state/delete_state.yml', methods=['DELETE'])
def delete_state(state_id):
    '''
        delete state obj given state_id
    '''
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
@swag_from('docs/state/create_state.yml', methods=['POST'])
def create_state():
    '''
        create new state obj
    '''
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    else:
        obj_data = request.get_json()
        obj = State(**obj_data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/states/<states_id>', methods=['PUT'], strict_slashes=False)
@swag_from('docs/state/update_state.yml', methods=['PUT'])
def update_state(states_id):
    '''
        update existing state object
    '''
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    obj = storage.get("State", states_id)
    if obj is None:
        abort(404)
    obj_data = request.get_json()
    obj.name = obj_data['name']
    obj.save()
    return jsonify(obj.to_dict()), 200
