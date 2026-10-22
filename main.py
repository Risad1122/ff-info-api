from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# WalkerZ API endpoint
SOURCE_API = "https://wzapi.vercel.app/get"

@app.route("/ff-info")
def ff_info():
    uid = request.args.get("uid", "").strip()
    region = request.args.get("region", "BD").strip().upper()

    if not uid:
        return jsonify({"error": "uid parameter required"}), 400
    if not uid.isdigit():
        return jsonify({"error": "uid must be numeric"}), 400

    try:
        # WalkerZ API সঠিক ফরমেট: uid & region
        r = requests.get(
            SOURCE_API, 
            params={"uid": uid, "region": region}, 
            timeout=15
        )
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
        "usage": "/ff-info?uid=1782212746"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
