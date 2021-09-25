from flask import Flask, render_template, redirect, session, url_for, request
from flask.helpers import flash
from flask_mysqldb import MySQL
import MySQLdb.cursors


app = Flask(__name__)
app.secret_key = "super secret key"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'laundromat'

mysql = MySQL(app)

#------------------- INDEX PAGE----------------------

@app.route('/')
def index():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM useraccount WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('index.html', account=account)
    else:
        return render_template('index.html')


#------------------- ABOUT PAGE----------------------


@app.route('/about')
def about():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM useraccount WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('about.html', account=account)
    else:
        return render_template('about.html')


#------------------- Service PAGE----------------------


@app.route('/services')
def services():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM useraccount WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('services.html', account=account)
    else:
        return render_template('services.html')



#------------------- FAQ PAGE----------------------


@app.route('/faq')
def faq():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM useraccount WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('faq.html', account=account)
    else:
        return render_template('faq.html')



#------------------- Order PAGE----------------------




@app.route('/order')
def order():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM useraccount WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('order.html', account=account)
    else:
        return render_template('login.html')
    
@app.route('/order', methods=['POST','GET'])
def order_post():
    if request.method=='POST' :
        orderid = request.form['orderid']
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        services = request.form['services']
        date = request.form['date']
        timeslot = request.form['timeslot']
        address = request.form['address']
        landmark = request.form['landmark']
        status = request.form['status']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO orders VALUES (NULL,%s, %s, %s, %s, %s, %s, %s, %s,%s,%s)', (orderid,name, phone, email,services,date,timeslot,address,landmark,status))
        mysql.connection.commit()
        flash("Form Submitted Successfully")
        return redirect(url_for('inbox'))
    return render_template('login.html')



#------------------- Cancel Order PAGE----------------------



@app.route('/cancelorder', methods=['POST','GET'])
def cancel_order():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM useraccount WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
    if request.method=='POST' :
        name = request.form['name']
        orderid = request.form['orderid']
        phone = request.form['phone']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO cancellation VALUES (NULL,%s, %s, %s, %s)', (name,orderid, phone, email))
        mysql.connection.commit()
        flash("Form Submitted Successfully")
        return redirect(url_for('inbox'))
    return render_template('cancelorder.html', account=account)




#------------------- Profile PAGE----------------------




@app.route('/profile')
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM useraccount WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    else:
        return render_template('login.html')




#------------------- Inbox PAGE----------------------


        
@app.route('/inbox')
def inbox():
    if 'loggedin' in session:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM orders WHERE phone = %s', (session['phone'],))
            data = cursor.fetchall()
            cursor.close()
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM useraccount WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('inbox.html', account=account, order=data)
    else:
        return render_template('login.html')




#------------------- View PAGE----------------------




@app.route('/view/<id>', methods=['POST','GET'])
def get_order(id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM orders WHERE id = %s", [id])
        data = cursor.fetchall()
        cursor.close()
        print(data[0])
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM useraccount WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('view.html',account=account, order=data[0])




#------------------- Login PAGE----------------------




@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST' and 'phone' in request.form and 'password' in request.form:
        phone = request.form['phone']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM useraccount WHERE phone = %s AND password = %s', (phone, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['phone'] = account['phone']
            return redirect(url_for('index'))
    return render_template('login.html')



#------------------- Register PAGE----------------------




@app.route('/register', methods = ['POST','GET'])
def register():
    if request.method == 'POST' and 'name' in request.form and 'phone' in request.form and 'password' in request.form and 'email' in request.form:
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM useraccount WHERE phone = %s', (phone,))
        account = cursor.fetchone()
        if account:
            flash("OOPS! Account Already Exists!")
        else:
            cursor.execute('INSERT INTO useraccount VALUES (NULL,%s, %s, %s, %s)', (name, phone, email,password,))
            mysql.connection.commit()
            flash("CONGRACTULATIONS! You have Registered Successfully")
    elif request.method == 'POST':
        flash("Please fill the Form")
    return render_template('register.html')



#------------------- LOGOUT----------------------



@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('phone', None)
   return redirect(url_for('index'))



    
if __name__=='__main__':
    app.run(debug=True)