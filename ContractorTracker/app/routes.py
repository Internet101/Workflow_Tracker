from flask import Blueprint, render_template, jsonify, request, send_from_directory
import sqlite3
import os
from werkzeug.utils import secure_filename

# Path to your SQLite database
DB_PATH = 'contractor_tracker.db'

# Initialize the Blueprint
bp = Blueprint('main', __name__)

# Ensure the job packs folder exists
JOB_PACKS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'job_packs'))
os.makedirs(JOB_PACKS_FOLDER, exist_ok=True)
print(f"Job Packs Folder Path: {JOB_PACKS_FOLDER}")

# Ensure the database tables exist
def initialize_tables():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contracts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id TEXT NOT NULL,
                description TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT,
                location TEXT,
                job_pack_path TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS revenue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                contract_id TEXT NOT NULL,
                dwellings INTEGER NOT NULL,
                is_blown INTEGER NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                job_pack_path TEXT
            )
        ''')
        conn.commit()
        print("Database tables verified.")

initialize_tables()

@bp.route('/')
def home():
    """Render the Home page."""
    return render_template('home.html')

@bp.route('/contracts-and-revenue')
def contracts_and_revenue():
    """Render the Contracts and Revenue page."""
    return render_template('revenue.html')

@bp.route('/contracts-data', methods=['GET'])
def get_contracts():
    """Fetch all contract records."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, job_id, description, start_date, end_date, location, job_pack_path FROM contracts')
            contracts = cursor.fetchall()

        formatted_contracts = [
            {
                "id": row[0],
                "job_id": row[1],
                "description": row[2],
                "start_date": row[3],
                "end_date": row[4],
                "location": row[5],
                "job_pack_path": row[6]
            }
            for row in contracts
        ]
        return jsonify({"contracts": formatted_contracts})
    except Exception as e:
        print(f"Error fetching contracts: {e}")
        return jsonify({"error": str(e)}), 500

@bp.route('/job-packs/<filename>')
def serve_job_pack(filename):
    """Serve a specific job pack PDF."""
    try:
        print(f"Attempting to serve file: {filename}")
        return send_from_directory(JOB_PACKS_FOLDER, filename, as_attachment=False)
    except Exception as e:
        print(f"Error serving file {filename}: {e}")
        return jsonify({"error": "File not found"}), 404

@bp.route('/contracts', methods=['POST'])
def add_job():
    """Add a new job to the database."""
    try:
        data = request.form
        file = request.files.get('job_pack')

        # Validate required fields
        required_fields = ['job_id', 'description', 'start_date', 'location']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"'{field}' is required"}), 400

        # Handle file upload
        job_pack_path = None
        if file and file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            job_pack_path = os.path.join(JOB_PACKS_FOLDER, filename)
            file.save(job_pack_path)

        # Insert into the database
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO contracts (job_id, description, start_date, end_date, location, job_pack_path)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (data['job_id'], data['description'], data['start_date'], data.get('end_date'), data['location'], job_pack_path))
            conn.commit()

        return jsonify({"message": "Job added successfully!"}), 201
    except Exception as e:
        print(f"Error adding job: {e}")
        return jsonify({"error": str(e)}), 500

@bp.route('/revenue-data', methods=['GET'])
def revenue_data_api():
    """Fetch all revenue records from the database."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, user_id, contract_id, dwellings, is_blown, amount, date, job_pack_path FROM revenue')
            revenue_records = cursor.fetchall()

        formatted_revenue = [
            {
                "id": row[0],
                "user_id": row[1],
                "contract_id": row[2],
                "dwellings": row[3],
                "is_blown": bool(row[4]),
                "amount": row[5],
                "date": row[6],
                "job_pack_path": row[7]
            }
            for row in revenue_records
        ]
        return jsonify({"revenue": formatted_revenue})
    except Exception as e:
        print(f"Error fetching revenue data: {e}")
        return jsonify({"error": str(e)}), 500

print(f"Using database: {DB_PATH}")
