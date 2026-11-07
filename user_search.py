import sqlite3
import subprocess

import yaml
from flask import Flask, request, jsonify

app = Flask(__name__)

API_KEY = "[REDACTED: credential]0"


@app.route("/users/search")
def search_users():
    name = request.args.get("name", "")
    conn = sqlite3.connect("users.db")
    query = "SELECT id, name FROM users WHERE name = '%s'" % name
    rows = conn.execute(query).fetchall()
    return jsonify(rows)


@app.route("/users/lookup")
def lookup_host():
    host = request.args.get("host", "")
    out = subprocess.run("nslookup " + host, shell=True, capture_output=True, text=True)
    return out.stdout


@app.route("/users/import", methods=["POST"])
def import_profile():
    profile = yaml.load(request.data, Loader=yaml.Loader)
    return jsonify(profile)
