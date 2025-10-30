import os
import csv
from datetime import datetime
from typing import Any, Dict

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from dotenv import load_dotenv
from supabase import create_client, Client


def load_env_and_create_supabase() -> Client:
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        print("⚠️  WARNING: Missing SUPABASE_URL or SUPABASE_ANON_KEY environment variables")
        print("⚠️  Data upload/download features will not work")
        print("⚠️  Please set these variables in Vercel dashboard: Settings > Environment Variables")
        return None
    return create_client(url, key)


supabase: Client = load_env_and_create_supabase()

app = Flask(__name__)
# Enable CORS for all origins (required for Vercel deployment)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type"]}})


def serve_html_file(filename):
    """Helper function to serve HTML files from root directory"""
    try:
        # Get the parent directory (project root) from api folder
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, filename)
        
        # Check if file exists
        if os.path.exists(file_path):
            # Try send_file first
            try:
                return send_file(file_path)
            except:
                # Fallback: read and return content directly
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return content, 200, {'Content-Type': 'text/html'}
        else:
            app.logger.error(f"File not found: {file_path}")
            return jsonify({"error": "File not found", "path": filename}), 404
    except Exception as e:
        app.logger.error(f"Error serving {filename}: {e}")
        return jsonify({"error": "Server error", "details": str(e)}), 500


@app.route("/")
def index():
    """Serve the login page"""
    return serve_html_file("login.html")


@app.route("/dashboard.html")
def dashboard():
    """Serve the dashboard page"""
    return serve_html_file("dashboard.html")


@app.route("/login.html")
def login_page():
    """Serve the login page"""
    return serve_html_file("login.html")


@app.route("/favicon.ico")
def favicon():
    """Serve favicon"""
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        favicon_path = os.path.join(base_dir, "public", "favicon.ico")
        
        if os.path.exists(favicon_path):
            return send_file(favicon_path, mimetype='image/x-icon')
        else:
            # Return 204 No Content for missing favicon
            return '', 204
    except Exception as e:
        app.logger.error(f"Error serving favicon: {e}")
        return '', 204


@app.post("/login")
def login():
    """Hardcoded authentication for cowcollar user"""
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or data.get("device_id") or "").strip()
    password = (data.get("password") or "").strip()

    # Hardcoded credentials
    CORRECT_USERNAME = "cowcollar"
    CORRECT_PASSWORD = "Waleed_Abdullah56"

    # Validate credentials
    if not username or not password:
        return jsonify({"success": False, "message": "Missing username or password"}), 400

    if username == CORRECT_USERNAME and password == CORRECT_PASSWORD:
        return jsonify({
            "success": True, 
            "message": "Login successful", 
            "username": username
        }), 200
    else:
        return jsonify({
            "success": False, 
            "message": "Invalid username or password"
        }), 401


@app.get("/data")
def get_data():
    """Fetch CSV data from Supabase Storage and return as JSON"""
    # Check if Supabase is configured
    if supabase is None:
        return jsonify({
            "success": False,
            "message": "Supabase not configured. Please set SUPABASE_URL and SUPABASE_ANON_KEY environment variables."
        }), 503
    
    data_rows = []
    
    # Try to download from Supabase
    try:
        bucket = os.getenv("SUPABASE_BUCKET", "datacollection")
        response = supabase.storage.from_(bucket).download("data.csv")
        
        if response:
            csv_content = response.decode("utf-8")
            lines = csv_content.strip().split("\n")
            
            if len(lines) > 1:
                reader = csv.DictReader(lines)
                for row in reader:
                    try:
                        data_rows.append({
                            "timestamp": row.get("timestamp", ""),
                            "device_id": row.get("device_id", ""),
                            "temperature": float(row.get("temperature", 0)),
                            "gyro_x": float(row.get("gyro_x", 0)),
                            "gyro_y": float(row.get("gyro_y", 0)),
                            "gyro_z": float(row.get("gyro_z", 0)),
                        })
                    except (ValueError, TypeError):
                        continue
                
                print(f"✓ Successfully read {len(data_rows)} rows from Supabase Storage")
                return jsonify({"success": True, "data": data_rows, "source": "supabase"}), 200
    except Exception as e:
        print(f"ℹ️  No data file found in Supabase (this is normal if no data has been uploaded yet): {e}")
    
    # No data available - return empty but successful response
    return jsonify({
        "success": True, 
        "data": [], 
        "message": "No data has been uploaded yet. Upload sensor data to see it here.",
        "source": "empty"
    }), 200


@app.post("/upload")
def upload():
    """Upload sensor data directly to Supabase Storage CSV (cloud-only, no local file)"""
    # Check if Supabase is configured
    if supabase is None:
        return jsonify({
            "success": False,
            "message": "Supabase not configured. Please set SUPABASE_URL and SUPABASE_ANON_KEY environment variables."
        }), 503
    
    payload = request.get_json(silent=True) or {}

    device_id = (payload.get("device_id") or "").strip()
    temperature = payload.get("temperature")
    gyroscope = payload.get("gyroscope") or {}
    gyro_x = gyroscope.get("x")
    gyro_y = gyroscope.get("y")
    gyro_z = gyroscope.get("z")
    timestamp_str = payload.get("timestamp") or datetime.utcnow().isoformat()

    # Basic validation
    if not device_id:
        return jsonify({"success": False, "message": "device_id is required"}), 400
    try:
        float(temperature)
        float(gyro_x)
        float(gyro_y)
        float(gyro_z)
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "temperature and gyroscope x,y,z must be numbers"}), 400

    # Normalize timestamp
    try:
        _ = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
    except Exception:
        return jsonify({"success": False, "message": "timestamp must be ISO 8601"}), 400

    # Download existing CSV from Supabase
    bucket = os.getenv("SUPABASE_BUCKET", "datacollection")
    try:
        response = supabase.storage.from_(bucket).download("data.csv")
        existing_csv = response.decode("utf-8") if response else ""
    except Exception as e:
        print(f"No existing CSV, creating new: {e}")
        existing_csv = "timestamp,device_id,temperature,gyro_x,gyro_y,gyro_z\n"
    
    # Append new row
    new_row = f"{timestamp_str},{device_id},{temperature},{gyro_x},{gyro_y},{gyro_z}\n"
    updated_csv = existing_csv + new_row
    
    # Upload back to Supabase
    try:
        supabase.storage.from_(bucket).upload(
            file=updated_csv.encode('utf-8'),
            path="data.csv",
            file_options={
                "content-type": "text/csv",
                "x-upsert": "true",
                "cache-control": "no-cache"
            }
        )
        print(f"✓ Data appended to Supabase Storage (device: {device_id})")
        return jsonify({"success": True, "message": "Data uploaded to cloud"}), 200
    except Exception as e:
        print(f"❌ Failed to upload to Supabase: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


#if __name__ == "__main__":
#   app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)


