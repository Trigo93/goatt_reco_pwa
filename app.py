from flask import Flask, request, jsonify, render_template
from pyairtable import Table
import os

# Get secret variables
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE = os.getenv('AIRTABLE_BASE')

app = Flask(__name__)

# FIXME: You can do better
AGE = ["moins de 12ans", "entre 12ans et 60ans", "plus de 60ans"]
PLAY_FREQ = ["rarement", "parfois", "souvent"]
BREAK_FREQ = ["rarement", "parfois", "souvent"]
GOAL = ["confort", "solidite", "performance"]


# Private methods
def is_data_consistent(data):
    return (data["age"] in AGE and data["play_freq"] in PLAY_FREQ
            and data["break_freq"] in BREAK_FREQ and data["goal"] in GOAL)


def get_strings(reco):
    try:
        table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE, 'strings')
        fields = table.all(sort=["id"])[reco - 1]["fields"]
    except:
        print("could not access database, please check api key and base name")
        print(AIRTABLE_API_KEY)
        return None

    strings = {}
    try:
        for i in range(3):  # number of recommendations
            prefix = "string_" + str(i + 1)
            strings[prefix] = {
                "name": fields[prefix + "_name"][0],
                "price": fields[prefix + "_price"][0],
                "image": fields[prefix + "_image"][0]["url"],
                "description": fields[prefix + "_description"][0],
            }
    except KeyError:
        print(
            "key error when accessing data base, sending a slack message...\n",
            fields)
        return None

    return strings


def process(data):
    reco = -1

    if not is_data_consistent(data):
        return reco

    # aliases
    age = data["age"]
    pf = data["play_freq"]
    bf = data["break_freq"]
    goal = data["goal"]
    is_injured = data["injury"]

    # Edges cases recommendation
    if age == "moins de 12ans":  # young player
        reco = 8
    elif age == "plus de 60ans":  # old player
        reco = 10
    elif is_injured:  # injured player
        if pf == "rarement" or pf == "parfois":
            reco = 10
        else:
            reco = 7
    # Recommendation algorithm
    else:
        if pf == "rarement":
            if bf == "rarement":
                if goal == "confort":
                    reco = 1
                elif goal == "solidite":
                    reco = 2
                elif goal == "performance":
                    reco = 3
            else:  # bf == "parfois" or bf == "souvent"
                if goal == "confort":
                    reco = 4
                elif goal == "solidite":
                    reco = 5
                elif goal == "performance":
                    reco = 6

        if pf == "parfois":
            if bf == "rarement":
                if goal == "confort":
                    reco = 3
                elif goal == "solidite":
                    reco = 2
                elif goal == "performance":
                    reco = 3
            elif bf == "parfois":
                if goal == "confort":
                    reco = 2
                elif goal == "solidite":
                    reco = 9
                elif goal == "performance":
                    reco = 6
            elif bf == "souvent":
                if goal == "confort":
                    reco = 4
                elif goal == "solidite":
                    reco = 5
                elif goal == "performance":
                    reco = 6

        if pf == "souvent":
            if bf == "rarement":
                if goal == "confort":
                    reco = 3
                elif goal == "solidite":
                    reco = 9
                elif goal == "performance":
                    reco = 3
            else:  # bf == "parfois" or bf == "souvent"
                if goal == "confort":
                    reco = 2
                elif goal == "solidite":
                    reco = 5
                elif goal == "performance":
                    reco = 6

    return reco


# Flask routes
@app.route("/")
def index():
    return render_template('form.html')


@app.route('/form/')
def form():
    return render_template('form.html')


@app.route('/algorithm/', methods=['POST', 'GET'])
def algorithm():
    if request.method == 'GET':
        data = {
            "age": request.args.get('age', type=str),
            "injury": request.args.get('injury', default=False, type=bool),
            "play_freq": request.args.get('play_freq', type=str),
            "break_freq": request.args.get('break_freq', type=str),
            "goal": request.args.get('goal', type=str)
        }

    elif request.method == 'POST':
        data = {
            "age": request.form.get('age', type=str),
            "injury": request.form.get('injury', default=False, type=bool),
            "play_freq": request.form.get('play_freq', type=str),
            "break_freq": request.form.get('break_freq', type=str),
            "goal": request.form.get('goal', type=str)
        }

    else:
        return jsonify(isError=True, message="Wrong request method")

    reco = process(data)
    strings = get_strings(reco)

    return jsonify(isError=(reco < 0),
                   input=data,
                   message="Invalid input data" if (reco < 0) else strings,
                   reco=reco), 200


@app.route('/recommendation/', methods=['POST', 'GET'])
def recommendation():
    if request.method == 'GET':
        data = {
            "age": request.args.get('age', type=str),
            "injury": request.args.get('injury', default=False, type=bool),
            "play_freq": request.args.get('play_freq', type=str),
            "break_freq": request.args.get('break_freq', type=str),
            "goal": request.args.get('goal', type=str)
        }

    elif request.method == 'POST':
        data = {
            "age": request.form.get('age', type=str),
            "injury": request.form.get('injury', default=False, type=bool),
            "play_freq": request.form.get('play_freq', type=str),
            "break_freq": request.form.get('break_freq', type=str),
            "goal": request.form.get('goal', type=str)
        }

    else:
        return jsonify(isError=True, message="Wrong request method")

    reco = process(data)
    if reco < 0:
        return jsonify(isError=True,
                       input=data,
                       message="Invalid input data",
                       reco=reco), 400

    strings = get_strings(reco)

    if strings is None:
        return jsonify(isError=True,
                       input=data,
                       message="Could not access database",
                       reco=reco), 400

    return render_template('result.html', data=data, results=strings)
