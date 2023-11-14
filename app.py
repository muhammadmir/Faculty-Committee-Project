from flask import Flask, request, Response
from flask_cors import CORS
from json import dumps
from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector.cursor import MySQLCursor

load_dotenv()

app = Flask(__name__)
CORS(app)

config = {
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASS"),
    "host": os.getenv("MYSQL_HOST"),
    "database": os.getenv("MYSQL_DB"),
    "connection_timeout": 10,
    "raise_on_warnings": True,
}

CNX = mysql.connector.connect(**config)

def faculty_attribute_lookup(cursor: MySQLCursor, faculty_name: str):
    attributes = []
    query = "SELECT * FROM Faculty WHERE FacultyName = %s"

    try:
        cursor.execute(query, (faculty_name,))
        for f_id, name, department, affiliaton, title in cursor.fetchall():
            faculty = {
                "ID": f_id,
                "Department": department,
                "Affiliation": affiliaton,
                "Title": title,
            }
            attributes.append(faculty)
    except Exception as e:
        print(f"Faculty Attribute Lookup | Error: {e}")
    return attributes

def committee_lookup(cursor: MySQLCursor, committee_code: str):
    committee = {}
    query = "SELECT * FROM Committee WHERE CommitteeCode = %s"

    try:
        cursor.execute(query, (committee_code,))
        for c_id, designation, code, name, c_type in cursor.fetchall():
            committee["ID"] = c_id
            committee["Designation"] = designation
            committee["Code"] = code
            committee["Name"] = name
            committee["Type"] = c_type
    except Exception as e:
        print(f"Committee Lookup | Error: {e}")
    return committee

def format_faculty_table():
    cursor = CNX.cursor()
    results = []
    query = "SELECT * FROM Faculty"

    try:
        cursor.execute(query)
        for f_id, name, department, affiliation, title in cursor.fetchall():
            faculty = {
                "ID": f_id,
                "Name": name,
                "Department": department,
                "Affiliation": affiliation,
                "Title": title,
            }
            results.append(faculty)
    except Exception as e:
        print(f"Format Faculty Table | Error: {e}")

    cursor.close()
    return results

def format_committee_table():
    cursor = CNX.cursor()
    results = []
    query = "SELECT * FROM Committee"

    try:
        cursor.execute(query)
        for c_id, designation, code, name, c_type in cursor.fetchall():
            committee = {
                "ID": c_id,
                "Name": name,
                "Code": code,
                "Designation": designation,
                "Type": c_type,
            }
            results.append(committee)
    except Exception as e:
        print(f"Format Committee Table | Error: {e}")

    cursor.close()
    return results

def format_relation_table():
    cursor = CNX.cursor()
    results = []
    query = "SELECT * FROM Relation"

    try:
        cursor.execute(query)
        for r_id, faculty_name, committee_code, serving_period in cursor.fetchall():
            faculty_attribute_obj = faculty_attribute_lookup(cursor, faculty_name)
            committee_obj = committee_lookup(cursor, committee_code)
            committee_obj["Until"] = serving_period

            relation = {
                "ID": r_id,
                "Name": faculty_name,
                "Attributes": faculty_attribute_obj,
                "Committee": committee_obj,
            }
            results.append(relation)
    except Exception as e:
        print(f"Format Relation Table | Error: {e}")

    cursor.close()
    return results

def handle_getting(table: str):
    results = []
    cursor = CNX.cursor()

    columns = (
        "FacultyName, FacultyDepartment"
        if table == "Faculty"
        else "CommitteeName, CommitteeCode"
    )
    query = f"SELECT DISTINCT {columns} FROM {table}"

    try:
        cursor.execute(query)
        results = cursor.fetchall()
        if table == "Faculty":
            results = [
                {"Name": name, "Department": department}
                for (name, department) in results
            ]
        else:
            results = [{"Name": name, "Code": code} for (name, code) in results]
    except Exception as e:
        print(f"Table: {table} | Error: {e}")

    cursor.close()
    return results

def add_row(table: str, data: dict):
    cursor = CNX.cursor()
    output = {"Success": False}

    columns = ", ".join(data.keys())
    values = ", ".join(["%s"] * len(data))

    query = f"INSERT INTO {table} ({columns}) VALUES ({values})"

    try:
        cursor.execute(query, [value for value in data.values()])
        CNX.commit()
        output["Success"] = True
    except Exception as e:
        print(f"Add Row | Table: {table} | Error: {e}")
        output["Error"] = e

    cursor.close()
    return output

def edit_row(table: str, data: dict):
    cursor = CNX.cursor()
    output = {"Success": False}

    conditions = ""
    lookup_keys = data["Lookup Keys"]
    for lookup in lookup_keys:
        key = list(lookup.keys())[0]
        conditions += key + " = %s"
        conditions += " AND " if conditions.count("AND") < len(lookup_keys) - 1 else ""

    query = f'UPDATE {table} SET {data["Update Key"]} =' + " %s WHERE " + conditions

    try:
        cursor.execute(
            query,
            [data["Update Value"]] + [list(item.values())[0] for item in lookup_keys],
        )
        CNX.commit()
        output["Success"] = True
    except Exception as e:
        print(f"Edit Row | Table: {table} | Error: {e}")
        output["Error"] = e

    cursor.close()
    return output

def remove_row(table: str, data: dict):
    cursor = CNX.cursor()
    output = {"Success": False}

    prefix = ""
    for key in data.keys():
        prefix += key + " = %s"
        prefix += " AND " if prefix.count("AND") < len(data.keys()) - 1 else ""

    query = f"DELETE FROM {table} WHERE " + prefix

    try:
        cursor.execute(query, [value for value in data.values()])
        CNX.commit()
        output["Success"] = True
    except Exception as e:
        print(f"Remove Row | Table: {table} | Error: {e}")
        output["Error"] = e

    cursor.close()
    return output

@app.route("/add/<table>", methods=["POST"])
def add(table: str):
    output = {"Error": "Request was invalid"}

    if table in ["Faculty", "Committee", "Relation"] and request.is_json:
        # Faculty Keys: FacultyName, FacultyDepartment, FacultyAffiliation, FacultyTitle
        # Committee Keys: CommitteeDesignation, CommitteeCode, CommitteeName, CommitteeType
        # Relation Keys: FacultyName, CommitteeName, ServingPeriod
        payload = request.json
        output = add_row(table, payload)

    return Response(dumps(output), status=200, mimetype="application/json")

@app.route("/edit/<table>", methods=["POST"])
def edit(table: str):
    output = {"Error": "Request was invalid"}

    if table in ["Faculty", "Committee", "Relation"] and request.is_json:
        # Keys: Lookup Keys (list), Update Key (str), Update Value (str)
        payload = request.json
        output = edit_row(table, payload)

    return Response(dumps(output), status=200, mimetype="application/json")

@app.route("/remove/<table>", methods=["POST"])
def remove(table: str):
    output = {"Error": "Request was invalid"}

    if table in ["Faculty", "Committee", "Relation"] and request.is_json:
        # Faculty Keys: FacultyName, FacultyDepartment
        # Committee Keys: CommitteeName
        # Relation Keys: FacultyName, CommitteeCode
        payload = request.json
        output = remove_row(table, payload)

    return Response(dumps(output), status=200, mimetype="application/json")

@app.route("/get/<table>", methods=["GET"])
def get(table: str):
    faculty_data = handle_getting("Faculty")
    committee_data = handle_getting("Committee")

    table_data = None

    if table == "Faculty":
        table_data = format_faculty_table()
    elif table == "Committee":
        table_data = format_committee_table()
    elif table == "Relation":
        table_data = format_relation_table()

    output = {
        "Success": len(faculty_data) > 0
        and len(committee_data) > 0
        and table_data is not None,
        "Faculty": faculty_data,
        "Committee": committee_data,
        "Table": table_data,
    }

    return Response(dumps(output), status=200, mimetype="application/json")

app.run(host="0.0.0.0", debug=True)