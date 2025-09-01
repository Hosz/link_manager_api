from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def Hello():
    hello = {"status": "ok", "message": "API Link Manager no ar!"}
    return jsonify(hello)

if __name__ == "__main__":
    app.run(debug=True)