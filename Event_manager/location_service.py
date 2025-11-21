import time
import threading
import requests
from GUI import ErrorNotify
from flask import Flask, request, jsonify, render_template
 
__all__ = ["run_server"]

error_handler = ErrorNotify()
app = Flask(__name__, template_folder="../templates")

OPENCAGE_API_KEY = "5c93c2c618f64dae899135c2793d13ce"

latest_coords = None
address = None

@app.route("/")
def index():
    return render_template("location_request.html")

@app.route("/location", methods=["POST"])
def location():
    global latest_coords
    global address
    data = request.json
    lat, lon = data.get("lat"), data.get("lon")

    if lat is None or lon is None:
        return jsonify({"error": "Coordinates not provided"}), 400
    
    latest_coords = {"lat": lat, "lon": lon}

    address = get_address(lat,lon)
    if address:
        return jsonify({"address": address})
    else:
        return jsonify({"error": "Adress not found"}), 404
    
def get_address(lat, lon):
    try:
        r = requests.get(
            "https://api.opencagedata.com/geocode/v1/json",
            params={
                'q': f"{lat}, {lon}",
                "key": OPENCAGE_API_KEY,
                'language': 'en',
                'no_annotations': 1
            },
            timeout=10
        )
        r.raise_for_status()
        result = r.json()
        if result.get("results"):
            return result["results"][0].get("formatted")
    except Exception as e:
        error_handler.show_error(f"Error getting address: {e}")
    return None

def background_task():
    global address
    time.sleep(10)

    while True:
        if latest_coords is not None:
            lat = latest_coords["lat"]
            lon = latest_coords["lon"]
            address = get_address(lat, lon)
            if not address:
                error_handler.show_error("Could not update address.")
            time.sleep(300)

def run_server():
    threading.Thread(target=background_task, daemon=True).start()
    app.run(debug=True, use_reloader = False)