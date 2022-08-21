from flask import Flask,session,url_for, render_template, request,redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors
app = Flask(__name__, template_folder='templates')
app.secret_key="abcdefgh"
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'video_stream_db'
mysql = MySQL(app)
@app.route('/')
def index():
   log=False
   if 'email' in session:
      log=True
      return render_template('success.html',login=log)
   return render_template("list.html")
@app.route('/register', methods=['GET','POST'])
def register():
   curr=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
   if request.method == 'POST':
      session['email']=request.form['email']
      curr.execute("INSERT into users VALUES(%s,%s)",((request.form['email'],request.form['pass'])))
      mysql.connection.commit()
      curr.close()
      return redirect(url_for('index'))
   return render_template("register.html")
@app.route('/logout',methods=['GET'])
def logout():
   session.pop('email',None)
   return redirect(url_for('index'))

@app.route('/login',methods=['GET','POST'])
def login():
   curr=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
   
   if 'email' in session:
      return render_template('success.html')
   else:
      if request.method == 'POST':
         session['email'] = request.form['email']
         curr.execute("SELECT * FROM users WHERE Email=%s",(request.form['email'],))
         data=curr.fetchall()
         if(data[0]['password']==request.form['pass']):
            return redirect(url_for('index'))
         else:
            return render_template('login.html')
   return render_template('login.html')
@app.route('/add',methods=['POST','GET'])
def add():
   if request.method=='POST':
      name=request.form['name']
      caption=request.form['capt']
      video=request.form['video']
      curr=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      curr.execute("INSERT into videos VALUES(%s,%s,%s)",(name,caption,video))
      mysql.connection.commit()
      curr.close()
      return redirect(url_for('index'))
   return render_template('upload_video.html')
if __name__ == '__main__':
   app.run(debug = True)