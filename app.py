from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Hello from Raspberry Pi! 🎉</h1><p>If you see this, Flask is working.</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
