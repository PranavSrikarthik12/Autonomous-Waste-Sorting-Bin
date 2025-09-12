from flask import Flask, jsonify, render_template_string
import main  # import shared state from main.py

app = Flask(__name__)

# Minimal dashboard template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Waste Bin Dashboard</title>
    <meta http-equiv="refresh" content="2">
</head>
<body>
    <h1>Autonomous Waste Bin Dashboard</h1>
    <p><b>Latest Status:</b> {{ status }}</p>
    <p><b>Confidence:</b> {{ confidence }}</p>
    <p><b>Timestamp:</b> {{ timestamp }}</p>
    <p><b>Total Items:</b> {{ total }}</p>
    <p><b>Bio Count:</b> {{ bio }}</p>
    <p><b>Non-Bio Count:</b> {{ nonbio }}</p>
</body>
</html>
"""

@app.route("/")
def dashboard():
    return render_template_string(
        HTML_TEMPLATE,
        status=main.latest_status["status"],
        confidence=main.latest_status["confidence"],
        timestamp=main.latest_status["timestamp"],
        total=main.latest_status["total_count"],
        bio=main.latest_status["bio_count"],
        nonbio=main.latest_status["nonbio_count"]
    )

@app.route("/api/status")
def api_status():
    return jsonify(main.latest_status)

def run_server():
    app.run(host="0.0.0.0", port=5000)
