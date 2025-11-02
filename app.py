from flask import Flask, request, jsonify, Response, render_template
from datetime import datetime
import os
import json

app = Flask(__name__, template_folder="templates")
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# Function to load data from data/MM-DD.json
def load_data(month, day):
    file_name = f"{month:02d}-{day:02d}.json"
    file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Serve homepage
@app.route("/")
def homepage():
    return render_template("index.html")

# Endpoint: /date → today’s data
@app.route("/date")
def today_data():
    now = datetime.now()
    month = now.month
    day = now.day
    data = load_data(month, day)
    if data is None:
        return jsonify({"error": "Date not found"}), 404

    callback = request.args.get("callback")
    json_data = json.dumps(data, ensure_ascii=False)
    if callback:
        return Response(f"{callback}({json_data})", mimetype="application/javascript; charset=utf-8")
    return Response(json_data, mimetype="application/json; charset=utf-8")

# Endpoint: /date/:month/:day
@app.route("/date/<int:month>/<int:day>")
def specific_date(month, day):
    data = load_data(month, day)
    if data is None:
        return jsonify({"error": "Date not found"}), 404

    callback = request.args.get("callback")
    json_data = json.dumps(data, ensure_ascii=False)
    if callback:
        return Response(f"{callback}({json_data})", mimetype="application/javascript; charset=utf-8")
    return Response(json_data, mimetype="application/json; charset=utf-8")

# Optional fallback for 404s
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
