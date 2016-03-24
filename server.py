from flask import Flask,render_template,url_for
from flask import request, session, g, redirect, abort, flash,jsonify
import os
import subprocess
app = Flask(__name__,static_folder='static',static_url_path='/static')
import pymysql.cursors

app.secret_key = os.urandom(24)
# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             # password='passwd',
                             db='efcoValveDoc',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cur=connection.cursor()
@app.route("/")
def index():
	flash('info','Welcome')
	return render_template('index.html',current_page="homepage")

@app.route('/showValves')
def showValves():
	cur.execute("select * from valves;")
	valves=cur.fetchall()
	return render_template('valves.html',valves=valves,current_page="valves")

@app.route('/valve/<valveNumber>')
def valveCard(valveNumber):
	sql="select * from valves where valve_id=%s"
	cur.execute(sql%(valveNumber))
	valveCard=cur.fetchall()
	return render_template('valveCard.html',valveCard=valveCard,current_page="valveCard")

@app.route('/startRPVI',methods=['GET'])
def startRPVI():
    command='C:\\Users\\kranthikiran\\Documents\\EFCO\\builds\EFCOTests\\releasePressure\\releasePressure.exe'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    print process.returncode
    return jsonify(done=200)

@app.route('/startSLVI',methods=['GET'])
def startSLVI():
    command='C:\\Users\\kranthikiran\\Documents\\EFCO\\builds\EFCOTests\\seatLeakage\\seatLeakage.exe'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    print process.returncode
    return jsonify(done=200)

if __name__ == "__main__":
    app.run(debug=True)
