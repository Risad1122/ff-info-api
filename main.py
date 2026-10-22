from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# নতুন সচল সোর্স API লিংক
SOURCE_API = "https://glob-info2.vercel.app/info"

@app.route("/ff-info")
def ff_info():
    uid = request.args.get("uid", "").strip()

    if not uid:
        return jsonify({"error": "uid parameter required"}), 400
    if not uid.isdigit():
        return jsonify({"error": "uid must be numeric"}), 400

    try:
        r = requests.get(SOURCE_API, params={"uid": uid}, timeout=15)
        r.raise_for_status()
        try:
            data = r.json()
        except ValueError:
            data = {"raw": r.text}
        return jsonify(data)
    except requests.exceptions.Timeout:
        return jsonify({"error": "source api timeout"}), 504
    except requests.exceptions.HTTPError as e:
        return jsonify({"error": f"source api error: {e.response.status_code}"}), e.response.status_code
    except requests.exceptions.RequestException:
        return jsonify({"error": "cannot reach source api"}), 502

@app.route("/")
def root():
    return jsonify({
        "status": "online",
        "brand": "Record BD",
        "developer": "Risad",
        "usage": "/ff-info?uid=305000592"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
