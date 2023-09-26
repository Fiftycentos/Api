from flask import Flask, request, jsonify
from json2xml import json2xml
import subprocess
import time
import sqlite3
import pandas as pd
import json


app = Flask(__name__)


def get_tables():
    try:
        conn = sqlite3.connect('adata_sqlite_erd.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM API_table_1;")
        names = list(map(lambda x: x[0], cursor.description))
        df = pd.DataFrame(cursor.fetchall(), columns=names)
        result = df.to_json(orient="records")
        parsed = json.loads(result)
        tables = json.dumps(parsed, indent=4, ensure_ascii=False)
        conn.close()
        return tables
    except Exception as e:
        return e


def create_tables():
    con = sqlite3.connect("adata_sqlite_erd.db")
    cursor = con.cursor()
    try:
        cursor.execute("""CREATE TABLE Organizations (
            ID INT PRIMARY KEY,
            Organization_Name VARCHAR(255),
            Full_Name VARCHAR(255),
            Territory VARCHAR(255),
            IIN VARCHAR(255)
        )
                    """)

        cursor.execute("""CREATE TABLE Court_Decisions (
            Decision_ID INT PRIMARY KEY,
            Organization_ID INT,
            Decision_Date DATE,
            Decision_Number VARCHAR(255),
            FOREIGN KEY (Organization_ID) REFERENCES Organizations(ID)
        )
                    """)

        cursor.execute("""CREATE TABLE Registration_History (
            Event_ID INT PRIMARY KEY,
            Organization_ID INT,
            Registration_Date DATE,
            Deregistration_Date DATE,
            FOREIGN KEY (Organization_ID) REFERENCES Organizations(ID)
        )
                    """)

        cursor.execute("""CREATE TABLE API_table_1 (
                    ID INT PRIMARY KEY,
                    Organization_name VARCHAR(255),
                    Full_name VARCHAR(255),
                    Territory VARCHAR(255),
                    IIN INT,
                    Court_decision VARCHAR(255),
                    Registration_Date DATE,
                    Deregistration_Date DATE,
                )
                            """)

    except:
        pass

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
        process = subprocess.Popen(['python', 'new_api_parser.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
    return tables, 200

@app.route('/')
def home():
    return 'Home'

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
