from flask import Flask, request, jsonify
from json2xml import json2xml
import subprocess
import time
import sqlite3

app = Flask(__name__)


def get_tables():
    try:
        conn = sqlite3.connect('adata_sqlite_erd.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Adata_data_task_2;")
        tables = cursor.fetchall()
        conn.close()
        return tables
    except Exception as e:
        return str(e)


@app.route('/json_to_xml', methods=['POST'])
def json_to_xml():
    try:
        if request.is_json:
            json_data = request.get_json()

            xml_data = json2xml.Json2xml(json_data).to_xml()

            return xml_data, 200, {'Content-Type': 'application/xml'}
        else:
            return 'Invalid JSON data', 400
    except Exception as e:
        return str(e), 500

@app.route('/start_parser', methods=['POST'])
def start_parser():
    try:
        start_time = time.time()
        process = subprocess.Popen(['python', 'new_parser.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stderr = process.communicate()
        end_time = time.time()
        runtime = end_time - start_time

        if process.returncode == 0:
            response = {
                "status": "success",
                "runtime": runtime,
                "message": "Parser completed successfully.",
            }
        else:
            response = {
                "status": "error",
                "runtime": runtime,
                "message": f"Parser failed with error: {stderr.decode('utf-8')}",
            }

        return jsonify(response), 200
    except Exception as e:
        return str(e), 500


@app.route('/show_table', methods=['GET'])
def show_table():
    tables = get_tables()
    if isinstance(tables, str):
        return jsonify({"error": tables}), 500
    else:
        return jsonify(tables), 200

if __name__ == '__main__':
    app.run(debug=True)