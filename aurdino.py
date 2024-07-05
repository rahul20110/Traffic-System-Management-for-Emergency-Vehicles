from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/signal', methods=['POST'])
def signal():
    data = request.json
    print(f"Received signal: {data}")
    # Simulate turning on an LED or similar
    return jsonify({"status": "Signal received"}), 200

if __name__ == '__main__':
    app.run(port=8080, debug=True)
