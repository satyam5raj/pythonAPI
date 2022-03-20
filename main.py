import psycopg2
from app import app
from db import init_pgconnection
from flask import jsonify
from flask import flash, request
# from werkzeug import generate_password_hash, check_password_hash
		
@app.route('/add', methods=['POST'])
def add_user():
	try:
		_json = request.json
		_username = _json['username']
		_email = _json['email']
		_password = _json['password']
		# validate the received values
		if _username and _email and _password and request.method == 'POST':
			#do not save password as a plain text
			# _hashed_password = generate_password_hash(_password)
			# save edits
			sql = "INSERT INTO account(username, password, email) VALUES(%s, %s, %s)"
			data = (_username, _password, _email,)
			conn = init_pgconnection()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User added successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


		
@app.route('/users', methods=['GET'])
def users():
	try:
		conn = init_pgconnection()
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM account")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/user/<id>', methods=['GET'])
def user(id):
	try:
        # id = id
		conn = init_pgconnection()
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM account WHERE id=%s", id)
		row = cursor.fetchone()
		resp = jsonify(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/update/<id>', methods=['PATCH'])
def update_user(id):
	try:
		_json = request.json
		# _id = _json['id']
		_username = _json['username']
		_email = _json['email']
		_password = _json['password']		
		# validate the received values
		if _username and _email and _password and id and request.method == 'PATCH':
			#do not save password as a plain text
			# _hashed_password = generate_password_hash(_password)
			# save edits
			sql = "UPDATE account SET username=%s, password=%s, email=%s WHERE id=%s"
			data = (_username, _password, _email, id,)
			conn = init_pgconnection()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User updated successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
	try:
		conn = init_pgconnection()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM account WHERE id=%s", (id,))
		conn.commit()
		resp = jsonify('User deleted successfully!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp
		
if __name__ == "__main__":
    app.run()