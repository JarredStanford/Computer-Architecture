#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *
from flask import Flask, jsonify, request

# Instantiate our Node
app = Flask(__name__)


@app.route('/binary', methods=['POST'])
def binary():
    values = request.get_json()
    required = ['binary']

    if not all(k in values for k in required):
        response = {'message': "Missing Values"}
        return jsonify(response), 400
    
    cpu = CPU()

    cpu.load(values['binary'])
    cpu.run()

    printouts = cpu.printouts
        
    response = {
        'message': printouts
    }

    return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)