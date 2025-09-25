from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, make_response, request, jsonify
from flask_cors import CORS
import sqlite3
import os

# Code obtained from ChatGPT site, personal login

app = Flask(__name__)
CORS(app)
app.wsgi_app = ProxyFix(app.wsgi_app)
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data.db')

ALLOWED_MEASURES = {
    "Violent crime rate",
    "Unemployment",
    "Children in poverty",
    "Diabetic screening",
    "Mammography screening",
    "Preventable hospital stays",
    "Uninsured",
    "Sexually transmitted infections",
    "Physical inactivity",
    "Adult obesity",
    "Premature Death",
    "Daily fine particulate matter"
}

def get_county_state_from_zip(zip_code):
    """Return (county_name, state_abbr) for a given ZIP code."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT county, state_abbreviation
        FROM zip_county
        WHERE zip = ?
    """, (zip_code,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0], row[1]
    return None, None

def get_health_measures(county_name, state_abbr, measure_name):
    """Return all health measures for a county and state filtered by measure_name."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT confidence_interval_lower_bound, confidence_interval_upper_bound,
               county, county_code, data_release_year, denominator, fipscode,
               measure_id, measure_name, numerator, raw_value, state, state_code, year_span
        FROM county_health_rankings
        WHERE county = ? AND state = ? AND Measure_name = ?
    """, (county_name, state_abbr, measure_name))
    rows = cursor.fetchall()
    conn.close()
    result = []
    for r in rows:
        result.append({
            "confidence_interval_lower_bound": r[0],
            "confidence_interval_upper_bound": r[1],
            "county": r[2],
            "county_code": r[3],
            "data_release_year": r[4],
            "denominator": r[5],
            "fipscode": r[6],
            "measure_id": r[7],
            "measure_name": r[8],
            "numerator": r[9],
            "raw_value": r[10],
            "state": r[11],
            "state_code": r[12],
            "year_span": r[13]
        })
    return result

@app.route('/county_data', methods=['POST'])
def county_data():
    data = request.get_json()

    # Error-handling: check for coffee=teapot
    if data.get("coffee") == "teapot":
        return "I'm a teapot", 418

    # Get data fields
    zip_code = data.get("zip")
    measure_name = data.get("measure_name")

    # Error-handling: did not supply either zip or measure name
    if not zip_code or not measure_name:
        return make_response(jsonify({"error": "Both 'zip' and 'measure_name' are required."}), 400)
    
    # Error: supplied a non-existent measure_name
    if measure_name not in ALLOWED_MEASURES:
        return make_response(jsonify({"error": f"Measure name not found. Must be one of {', '.join(ALLOWED_MEASURES)}"}), 404)

    # Error-handling: supplied a non-existent ZIP (does not have 5 digits) 
    if not zip_code.isdigit() or len(zip_code) != 5:
        return make_response(jsonify({"error": "ZIP code not found. ZIP must be a 5-digit number."}), 404)

    # Error-handling: supplied a non-existent ZIP (no associated data)
    county_name, state_abbr = get_county_state_from_zip(zip_code)
    if not county_name:
        return make_response(jsonify({"error": f"ZIP code not found.  No county found for ZIP {zip_code}."}), 404)

    # Error-handling: supplied a non-existent ZIP and measure-pair (no associated data)
    result = get_health_measures(county_name, state_abbr, measure_name)
    if not result:
        return make_response(jsonify({"error": f"No data found for ZIP {zip_code} and measure '{measure_name}'."}), 404)

    return jsonify(result)

@app.errorhandler(404)
def page_not_found(e):
    """ If an endpoint other than county_data is requested, return a 404 error. """
    return make_response(jsonify({"error": "Endpoint not allowed: must use county_data endpoint"}), 404)

# app.run(debug=True) # only for local development, disable for Vercel

