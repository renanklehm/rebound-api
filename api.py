from src.main import Simulation
from flask import Flask, jsonify, request

app = Flask("Rebound")
sim = Simulation()


@app.route('/')
def home():
    return 'This API should not be used in regular browser mode. Please use it as an API endpoint.'


@app.route('/create', methods=['POST'])
def create_route():
    global sim
    data = request.json
    result = {}
    if (data is None) or ('name' not in data):
        result = {'status': 'error', 'message': 'Please provide a name'}
    elif data['name'] == '':
        result = {'status': 'error', 'message': 'Please provide a non-null name'}
    else:
        sim = Simulation(data['name'])
        sim.save()
        result = {'status': 'success'}
    return jsonify(result)


@app.route('/load', methods=['POST'])
def load_route():
    global sim
    data = request.json
    result = {}
    if (data is None) or ('name' not in data):
        result = {'status': 'error', 'message': 'Please provide a name'}
    elif data['name'] == '':
        result = {'status': 'error', 'message': 'Please provide a non-null name'}
    else:
        try:
            sim = Simulation.load(data['name'])
            result = {'status': 'success'}
        except Exception as e:
            result = {'status': 'error', 'message': str(e)}
    return jsonify(result)


@app.route('/add_primary', methods=['POST'])
def add_primary_route():
    global sim
    data = request.json
    result = {}
    if (data is None) or ('m' not in data) or ('hash' not in data):
        result = {'status': 'error', 'message': 'Please provide mass and hash'}
    elif not isinstance(data['m'], (float, int)):
        result = {'status': 'error', 'message': 'Mass should be a float'}
    elif not isinstance(data['hash'], (str)):
        result = {'status': 'error', 'message': 'Hash should be a string'}
    elif sim.name == '':
        result = {'status': 'error', 'message': 'Please create a simulation first'}
    else:
        try:
            sim.add_primary(**data)
            sim.save()
            result = {'status': 'success'}
        except Exception as e:
            result = {'status': 'error', 'message': str(e)}
    return jsonify(result)


@app.route('/add_object', methods=['POST'])
def add_object_route():
    global sim
    data = request.json
    result = {}
    if (data is None) or ('m' not in data) or ('hash' not in data):
        result = {'status': 'error', 'message': 'Please provide mass and hash'}
    elif not isinstance(data['m'], (float, int)):
        result = {'status': 'error', 'message': 'Mass should be a float'}
    elif not isinstance(data['hash'], (str)):
        result = {'status': 'error', 'message': 'Hash should be a string'}
    elif sim.name == '':
        result = {'status': 'error', 'message': 'Please create a simulation first'}
    else:
        try:
            sim.add_object(**data)
            sim.save()
            result = {'status': 'success'}
        except Exception as e:
            result = {'status': 'error', 'message': str(e)}
    return jsonify(result)


@app.route('/add_from_orbital_elements', methods=['POST'])
def add_from_orbital_elements_route():
    global sim
    data = request.json
    result = {}
    if (data is None) or ('m' not in data) or ('hash' not in data):
        result = {'status': 'error', 'message': 'Please provide mass and hash'}
    elif not isinstance(data['m'], (float, int)):
        result = {'status': 'error', 'message': 'Mass should be a float'}
    elif not isinstance(data['hash'], (str)):
        result = {'status': 'error', 'message': 'Hash should be a string'}
    elif sim.name == '':
        result = {'status': 'error', 'message': 'Please create a simulation first'}
    else:
        try:
            sim.add_from_orbital_elements(**data)
            sim.save()
            result = {'status': 'success'}
        except Exception as e:
            result = {'status': 'error', 'message': str(e)}
    return jsonify(result)


@app.route('/integrate', methods=['POST'])
def integrate_route():
    global sim
    data = request.json
    result = {}
    if (data is None) or ('time' not in data):
        result = {'status': 'error', 'message': 'Please provide time'}
    elif not isinstance(data['time'], (float, int)):
        result = {'status': 'error', 'message': 'Time should be a float'}
    elif sim.name == '':
        result = {'status': 'error', 'message': 'Please create a simulation first'}
    else:
        try:
            result = sim.integrate(data['time'])
            sim.save()
        except Exception as e:
            result = {'status': 'error', 'message': str(e)}
    return jsonify(result)


@app.route('/get_trajectory', methods=['POST'])
def get_trajectory_route():
    global sim
    data = request.json
    result = {}
    if (data is None) or ('end_time' not in data) or ('time_step' not in data):
        result = {'status': 'error', 'message': 'Please provide end_time and time_step'}
    elif not isinstance(data['end_time'], (float, int)):
        result = {'status': 'error', 'message': 'End time should be a float'}
    elif not isinstance(data['time_step'], (float, int)):
        result = {'status': 'error', 'message': 'Time step should be a float'}
    elif sim.name == '':
        result = {'status': 'error', 'message': 'Please create a simulation first'}
    else:
        try:
            result = sim.get_trajectory(**data)
        except Exception as e:
            result = {'status': 'error', 'message': str(e)}
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4242)