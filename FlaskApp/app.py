from flask import Flask, render_template, json, request, redirect
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from flask import session
app = Flask(__name__)
mysql = MySQL()

#MySql configurations
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='fafhrd123'
app.config['MYSQL_DATABASE_DB']='Iedapp1'
app.config['MYSQL_DATABASE_HOST']='localhost'
mysql.init_app(app)

@app.route("/")
def main():
	return render_template('index.html')
@app.route('/showSignUp')
def showSignup():
	return render_template('signup.html')
@app.route('/signUp', methods = ['POST'])
def signUp():
	# read the posted values from the UI
	try:
		__userid = request.form['inputUserid']
		__name = request.form['inputName']
		__email = request.form['inputEmail']
		__password = request.form['inputPassword']

		if __name and __email and __password:
			conn = mysql.connect()
			cursor = conn.cursor()
			_hashed_password = generate_password_hash(__password)
			#print(_hashed_password)
			#cursor.callproc('sp_createUser',(__name,__email,_hashed_password))
			cursor.callproc('sp_createUser',(__userid,__name,__email,__password))
			data = cursor.fetchall()

			if len(data) is 0:
				conn.commit()
				return json.dumps({'message':'User created successfully !'})
			else:
				return json.dumps({'error':str(data[0])})
		else:
			return json.dumps({'html':'<span>Enter the required fields</span>'})

	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cursor.close() 
		conn.close()
@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
 
 
 
        # connect to mysql
 
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall() 
 
        if len(data) > 0:
            if (str(data[0][3])==_password):
                session['user'] = data[0][0]
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')
 
 
    except Exception as e:
        print(str(e))
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()
@app.route('/showSignin')
def showSignin():
	return render_template('signin.html')
@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')
@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')
@app.route('/getWish')
def getWish():
    try:
        if session.get('user'):
            _user = session.get('user')
            print("HOOOOLAAAAAAAAAAAA")
            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_GetWishByUser',(_user,))
            wishes = cursor.fetchall()
            print(wishes)
            wishes_dict = []
            for wish in wishes:
                wish_dict = {
                        'Id': wish[0],
                        'nam': wish[1],
                        'usernam': wish[2],
                        'passwor': wish[3],
                        'money':wish[4],
                        'reward':wish[5]}
                wishes_dict.append(wish_dict)
            print(json.dumps(wishes_dict))
            return json.dumps(wishes_dict)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error = str(e))
@app.route('/Showadd')
def showaddup():
	return render_template('sysadd.html')
@app.route('/add', methods = ['POST'])
def addUp():
	# read the posted values from the UI
	print("HOOOOLAAAAAAAAAAAA")
	try:
		__userid = request.form['inputUserid']
		__password = request.form['inputPassword']
		__monsub = request.form['submoney']
		__reward = request.form['addpoints']
		if __userid and __password:
			conn = mysql.connect()
			cursor = conn.cursor()
			_hashed_password = generate_password_hash(__password)
			#print(_hashed_password)
			#cursor.callproc('sp_createUser',(__name,__email,_hashed_password))
			cursor.callproc('sp_add',(__monsub,__reward,__userid))
			data = cursor.fetchall()

			if len(data) is 0:
				conn.commit()
				return json.dumps({'message':'Transaction Succesfull!'})
			else:
				return json.dumps({'error':str(data[0])})
		else:
			return json.dumps({'html':'<span>Enter the required fields</span>'})
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cursor.close() 
		conn.close()
@app.route('/add2', methods = ['POST'])
def addUp2():
	# read the posted values from the UI
	print("GGGGGGGGGGGGGGGGGGGGGAAAAAAAAAAAA")
	try:
		_username = request.form['inputEmail']
		__monsub = request.form['submoney']
		print(__monsub)
		if _username:
			_user = session.get('user')
			print("Hello")
			conn = mysql.connect()
			cursor = conn.cursor()
			#_hashed_password = generate_password_hash(__password)
			#print(_hashed_password)
			#cursor.callproc('sp_createUser',(__name,__email,_hashed_password))
			cursor.callproc('sp_addtoanother',(_user,__monsub,_username))
			data = cursor.fetchall()

			if len(data) is 0:
				conn.commit()
				return json.dumps({'message':'Transfer Succesfull!'})
			else:
				return json.dumps({'error':str(data[0])})
		else:
			return json.dumps({'html':'<span>Enter the required fields</span>'})
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cursor.close() 
		conn.close()

if __name__ == '__main__':
	app.secret_key = 'why would I tell you my secret key?'
	app.run(host='0.0.0.0', threaded=True, debug=True, port=5000)