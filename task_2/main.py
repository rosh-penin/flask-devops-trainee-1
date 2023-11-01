import json

from flask import Flask, jsonify, request
from redis import Redis

REDIS_HOST = 'redis'
REDIS_PORT = 6379

app = Flask(__name__)
db = Redis(REDIS_HOST, REDIS_PORT)


@app.get("/<string:key>")
def get_key(key):
    """Get json string from nosql db and returns them as json objects."""
    value = db.get(key)
    if not value:
        return jsonify({'error': 'Key not found'}), 404
    return jsonify(json.loads(value)), 200


@app.post("/<string:key>")
def create_key(key):
    """Accepts only json objects and save them as plain text."""
    data = request.get_data(as_text=True)
    if not data:
        return jsonify({'error': 'Invalid data'}), 400
    db.set(key, data)
    return jsonify(json.loads(data)), 201


@app.put("/<string:key>")
def update_key(key):
    """
    If there is no key - returns 404 error.
    Otherwise replace json string with another from request body.
    """
    if not db.exists(key):
        return jsonify({'error': 'Key not found'}), 404
    data = request.get_data(as_text=True)
    db.set(key, data)
    return jsonify(json.loads(data)), 200
