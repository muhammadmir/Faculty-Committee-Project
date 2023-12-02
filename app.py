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

def faculty_attribute_lookup(cursor: MySQLCursor, faculty_name: str) -> list[dict]:
    """Looks up all of the ID's, Department's, Affiliation's, and Title's associated with Faculty's Name in
    the Faculty Table. This function is exclusively used when formatting data for the Relation Page.

    Args:
        cursor (MySQLCursor): MySQLCursor Object.
        faculty_name (str): Faculty's Name.

    Returns:
        list[dict]: A list of dictonaries containing the attributes.
    """
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

def committee_lookup(cursor: MySQLCursor, committee_code: str) -> dict:
    """Look's up the Committee ID, Designation, Code, Name, and Type associated with the Committee Code in the
    Committee Table.

    Args:
        cursor (MySQLCursor): MySQLCursor Object.
        committee_code (str): Committee Code.

    Returns:
        dict: A dictionary object contataining the information regarding the Committee.
    """
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

def get_faculty_table() -> list[dict]:
    """Get's all the rows in the Faculty Table.

    Returns:
        list[dict]: A list of dictonaries containing the ID, Name, Department, Affiliation, and Title of
        each Faculty Member. 
    """
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

def get_committee_table() -> list[dict]:
    """Get's all the rows in the Committee Table.

    Returns:
        list[dict]: A list of dictonaries containing the ID, Name, Code, Designation, and Type of each
        each Committee. 
    """
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

def get_relation_table() -> list[dict]:
    """Get's all the rows in the Relation Table. 

    Returns:
        list[dict]: A list of dictonaries containing the ID and Name of the Relation, the Attributes associated
        with the Faculty Name, and the Committee information associated with the Relation.
    """
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

def handle_getting(table: str) -> list[dict]:
    """Get's a special list of dictonaries from the Faculty and Committee Tables that make the editing
    feature of the Faculty, Committee, and Relation Page's more easier.
    
    If the table is Faculty, then each dictonary object has the Name and Department of the Faculty Member.
    If the table is Committee, then each dictonary object has the Name and Code of the Commmittee. 

    Args:
        table (str): Either Faculty or Committee.

    Returns:
        list[dict]: A list of dictonaries containing the relevant information from the table.
    """
    results = []
    cursor = CNX.cursor()

    columns = "FacultyName, FacultyDepartment" if table == "Faculty" else "CommitteeName, CommitteeCode"
    query = f"SELECT DISTINCT {columns} FROM {table}"

    try:
        cursor.execute(query)
        results = cursor.fetchall()
        if table == "Faculty":
            results = [{"Name": name, "Department": department} for (name, department) in results]
        else:
            results = [{"Name": name, "Code": code} for (name, code) in results]
    except Exception as e:
        print(f"Table: {table} | Error: {e}")

    cursor.close()
    return results

def add_row(table: str, data: dict) -> dict:
    """Adds a row to the table.

    Args:
        table (str): Either Faculty, Committee, or Relation.
        data (dict): The appropriate data related to the table.

    Returns:
        dict: A dictonary containing the Success and Error keys, wherever applicable, indicating if
        the operation was successful or not and error associated with it.
    """
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

def edit_row(table: str, data: dict) -> dict:
    """Edits a row to the table.

    Args:
        table (str): Either Faculty, Committee, or Relation.
        data (dict): The appropriate data related to the table, including a key containing a list of
        lookup keys.

    Returns:
        dict: A dictonary containing the Success and Error keys, wherever applicable, indicating if the
        operation was successful or not and error associated with it.
    """
    cursor = CNX.cursor()
    output = {"Success": False}

    conditions = ""
    lookup_keys = data["Lookup Keys"]
    
    # Dynamically formats the list of look up keys in AND logic. 
    for lookup in lookup_keys:
        key = list(lookup.keys())[0]
        conditions += key + " = %s"
        conditions += " AND " if conditions.count("AND") < len(lookup_keys) - 1 else ""

    query = f'UPDATE {table} SET {data["Update Key"]} =' + " %s WHERE " + conditions

    try:
        cursor.execute(query, [data["Update Value"]] + [list(item.values())[0] for item in lookup_keys])
        CNX.commit()
        output["Success"] = True
    except Exception as e:
        print(f"Edit Row | Table: {table} | Error: {e}")
        output["Error"] = e

    cursor.close()
    return output

def remove_row(table: str, data: dict) -> dict:
    """Deletes a row to the table.

    Args:
        table (str): Either Faculty, Committee, or Relation.
        data (dict): The appropriate data related to the table, including a key containing a list of
        lookup keys.

    Returns:
        dict: A dictonary containing the Success and Error keys, wherever applicable, indicating if the
        operation was successful or not and error associated with it.
    """
    cursor = CNX.cursor()
    output = {"Success": False}

    prefix = ""
    
    # Dynamically formats the list of look up keys in AND logic. 
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
def add(table: str) -> Response:
    """Route to add row to a particular table.
    
    If table is Faculty, the expected keys are the following: FacultyName, FacultyDepartment,
    FacultyAffiliation, FacultyTitle.
    
    If table is Committee, the expected keys are the following: CommitteeDesignation, CommitteeCode,
    CommitteeName, CommitteeType.
    
    If the table is Relation, the expected keys are the following: FacultyName, CommitteeName,
    ServingPeriod.

    Args:
        table (str): Either Faculty, Commmittee, or Relation.

    Returns:
        Response: Return's a 200 JSON response.
    """
    output = {"Error": "Request was invalid"}

    if table in ["Faculty", "Committee", "Relation"] and request.is_json:
        payload = request.json
        output = add_row(table, payload)

    return Response(dumps(output), status=200, mimetype="application/json")

@app.route("/edit/<table>", methods=["POST"])
def edit(table: str) -> Response:
    """Route to edit row from a particular table.
    
    Regardles of the table, the expected keys are the following: Lookup Keys (list),
    Update Key (str), Update Value (str).
    
    Note: It is expected that the Lookup Keys and the the Update Key are present in the respective table.

    Args:
        table (str): Either Faculty, Commmittee, or Relation.

    Returns:
        Response: Return's a 200 JSON response.
    """
    output = {"Error": "Request was invalid"}

    if table in ["Faculty", "Committee", "Relation"] and request.is_json:
        # Keys: Lookup Keys (list), Update Key (str), Update Value (str)
        payload = request.json
        output = edit_row(table, payload)

    return Response(dumps(output), status=200, mimetype="application/json")

@app.route("/remove/<table>", methods=["POST"])
def remove(table: str) -> Response:
    """Route to remove row from a particular table.
    
    If table is Faculty, the expected keys are the following: FacultyName, FacultyDepartment.
    
    If table is Committee, the expected keys are the following: CommitteeName.
    
    If the table is Relation, the expected keys are the following: FacultyName, CommitteeCode.

    Args:
        table (str): Either Faculty, Commmittee, or Relation.

    Returns:
        Response: Return's a 200 JSON response.
    """
    output = {"Error": "Request was invalid"}

    if table in ["Faculty", "Committee", "Relation"] and request.is_json:
        # Faculty Keys: FacultyName, FacultyDepartment
        # Committee Keys: CommitteeName
        # Relation Keys: FacultyName, CommitteeCode
        payload = request.json
        output = remove_row(table, payload)

    return Response(dumps(output), status=200, mimetype="application/json")

@app.route("/get/<table>", methods=["GET"])
def get(table: str) -> Response:
    """Route to get all rows from a particular table.
    
    Args:
        table (str): Either Faculty, Commmittee, or Relation.

    Returns:
        Response: Return's a 200 JSON response.
    """
    faculty_data = handle_getting("Faculty")
    committee_data = handle_getting("Committee")

    table_data = None

    if table == "Faculty": table_data = get_faculty_table()
    elif table == "Committee": table_data = get_committee_table()
    elif table == "Relation": table_data = get_relation_table()

    output = {
        "Success": len(faculty_data) > 0 and len(committee_data) > 0 and table_data is not None,
        "Faculty": faculty_data,
        "Committee": committee_data,
        "Table": table_data,
    }

    return Response(dumps(output), status=200, mimetype="application/json")

app.run(host="0.0.0.0", port=5000, debug=True)