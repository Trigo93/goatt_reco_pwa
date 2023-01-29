from flask import Flask, request, jsonify, render_template, send_file

from static.scripts.algorithm import Recommendation
import static.scripts.airtable as airtable
import static.scripts.http as http

app = Flask(__name__)

# Flask routes
@app.route("/")
def index():
    return render_template('form.html')


@app.route('/recommendation/', methods=['POST', 'GET'])
def recommendation():
    data = http.process_request(request)

    if data is None:
        return jsonify(isError=True, message="Wrong request method")

    algo = Recommendation(data)
    reco = algo.process()

    if reco is None:
        return jsonify(isError=True,
                       input=data,
                       message="Invalid input data",
                       reco=reco), 400

    strings = airtable.get_strings(reco)

    if strings is None:
        return jsonify(isError=True,
                       input=data,
                       message="Could not access database",
                       reco=reco), 400

    return render_template('result.html', data=data, results=strings)

# PWA requirements
@app.route('/sw.js')
def serve_sw():
    return send_file('sw.js', mimetype='application/javascript')

@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype='application/manifest+json')

if __name__ == '__main__':
    app.run()
