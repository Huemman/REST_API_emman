import pymysql
from app import app
from config import mysql
from flask import jsonify, Request
from flask import flash, request



def employee_table_format():
    format = [
                {
                    "json Format": "CHECK FORMAT",
                    "REASONS": "Already exist in database or wrong Format"
                },
                {
                        
                        "birth_day": "YYYY-MM-DD",
                        "branch_id": "INT PRIMARY KEY",
                        "emp_id": "INTEGER",
                        "first_name": "Juan",
                        "last_name": "Dela Cruz",
                        "salary": "INTEGER",
                        "sex": "M or F"
                }
            ]
    response = jsonify(format)
    response.status_code = 400
    return response


@app.route('/<string:password>')
def auth(password):
    if password == '1234':
        url = {
            "methods_GET":
                {
                    "employee_table": "/employee",
                    "get_specific_employee": "/employee/<int:emp_id>"                    
                },
            "methods_POST":
                {   
                    "add_employee": "/employee/add"
                },
            "methods_PUT":
                {   
                    "update_employee_details": "/employee/update"
                },
            "methods_DELETE":
                {
                    "remove_employee": "/delete/<int:emp_id>"
                }
            }
        return jsonify(url)
    else:
        return jsonify('wrong password')


##############################-READ Table-###############################


@app.route('/employee')
def employee():
    try:
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * FROM employee")
        rows = cur.fetchall()
        response = jsonify(rows)
        response.status_code = 200
    except Exception as e:
        print(e)
    finally:
        cur.close() 
        conn.close()
        return response


@app.route('/employee/<int:emp_id>')
def get_emp_id(emp_id):
    try:
        app.logger.debug("Fetch employee with ID: %s", emp_id)
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        data = f"SELECT * FROM employee WHERE emp_id = {emp_id}"
        cur.execute(data)
        rows = cur.fetchall()
        response = jsonify(rows)
        response.status_code = 200
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()
        return response


##############################-CREATE employee-###############################


@app.route('/employee/add', methods=['POST'])
def add_employee():     
    try:
        _json = request.json
        _emp_id = _json['emp_id']
        _first_name = _json['first_name']
        _last_name = _json['last_name']
        _birth_day = _json['birth_day']
        _sex = _json['sex']
        _salary = _json['salary']	
        _branch_id = _json['branch_id']		

        if _emp_id and _first_name and _last_name and _birth_day and _sex and _salary and _branch_id and request.method == 'POST':
            employee = "INSERT INTO employee(emp_id, first_name, last_name, birth_day, sex, salary, branch_id) VALUES(%s, %s, %s, %s, %s, %s, %s)"
            details = (_emp_id, _first_name, _last_name, _birth_day, _sex, _salary, _branch_id)            
            try:
                conn = mysql.connect()
                cur = conn.cursor(pymysql.cursors.DictCursor)
                cur.execute(employee, details)
                conn.commit()
                response = jsonify('Employee added successfully!')
                response.status_code = 200
                return response
            except Exception as e:
                print(e)
                return employee_table_format()
            finally:
                cur.close()
                conn.close() 
        else:
            return jsonify('Not a method POST request')
    except Exception as e:
        print(e)


##############################-UPDATE table-###############################


@app.route('/employee/update', methods=['PUT'])
def update_table():     
    try:
        _json = request.json
        _emp_id = _json['emp_id']
        _first_name = _json['first_name']
        _last_name = _json['last_name']
        _birth_day = _json['birth_day']
        _sex = _json['sex']
        _salary = _json['salary']	
        _branch_id = _json['branch_id']		

        if _emp_id and _first_name and _last_name and _birth_day and _sex and _salary and _branch_id and request.method == 'PUT':
            employee = "UPDATE employee SET emp_id=%s, first_name=%s, last_name=%s, birth_day=%s, sex=%s, salary=%s, branch_id=%s WHERE emp_id=%s"
            details = (_emp_id, _first_name, _last_name, _birth_day, _sex, _salary, _branch_id, _emp_id)                   
            try:
                conn = mysql.connect()
                cur = conn.cursor(pymysql.cursors.DictCursor)
                cur.execute(employee, details)
                conn.commit()
                response = jsonify('table updated successfully!')
                response.status_code = 200
                return response
            except Exception as e:
                print(e)
                return employee_table_format()
            finally:
                cur.close()
                conn.close() 
        else:
            return jsonify('Not a method PUT request')
    except Exception as e:
        print(e)

##############################-DELETE employee-###############################


@app.route('/delete/<int:emp_id>', methods=['DELETE'])
def delete_emp(emp_id):
    
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("DELETE FROM employee WHERE emp_id =%s", (emp_id,))
        conn.commit()
        response = jsonify('Employee removed from table')
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 

if __name__ == ('__main__'):
    app.run(debug=True)
