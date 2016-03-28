from flask import Flask,render_template,url_for
from flask import request, session, g, redirect, abort, flash,jsonify
import os
from bs4 import BeautifulSoup
import subprocess
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,static_folder='static',static_url_path='/static')
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/efco'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)

class Valve(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    valve_id=db.Column(db.String(32))
    valve_type=db.Column(db.String(32))
    rev_no=db.Column(db.String(16))
    part_no=db.Column(db.String(16))
    install_locations=db.Column(db.String(32))
    customer=db.Column(db.String(100))
    manufacturer=db.Column(db.String(100))
    manufacturer_no=db.Column(db.String(64))
    plant=db.Column(db.String(32))
    createdOn=db.Column(db.DateTime)

    def __init__(self,valve_id,valve_type,rev_no,part_no,install_locations,customer,manufacturer,manufacturer_no,plant):
        self.valve_id=valve_id
        self.valve_type=valve_type
        self.rev_no=rev_no
        self.part_no=part_no
        self.install_locations=install_locations
        self.customer=customer
        self.manufacturer=manufacturer
        self.manufacturer_no=manufacturer_no
        self.plant=plant
        self.createdOn=datetime.now()
    def __repr__(self):
        return '<Valve %r>'% self.valve_id
class ValveTestData(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    valve_id=db.Column(db.String(32))
    inspector=db.Column(db.String(32))
    testLocation=db.Column(db.String(32))
    testMedium=db.Column(db.String(32))
    applicationNumber=db.Column(db.String(32))
    surveyor=db.Column(db.String(32))
    pressureTransducer=db.Column(db.String(32))
    certificationNumber=db.Column(db.String(32))
    testDate=db.Column(db.DateTime)

    def __init__(self,valve_id,inspector,testLocation,testMedium,applicationNumber,surveyor,pressureTransducer,certificationNumber,testDate):
        self.valve_id=valve_id
        self.inspector=inspector
        self.testLocation=testLocation
        self.testMedium=testMedium
        self.applicationNumber=applicationNumber
        self.surveyor=surveyor
        self.pressureTransducer=pressureTransducer
        self.certificationNumber=certificationNumber
        self.testDate=testDate
    def __repr__(self):
        return '<ValveTestData %r'%self.valve_id
class ValveTechincalData(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    valve_id=db.Column(db.String(32))
    dnInlet=db.Column(db.Float)
    dnOutlet=db.Column(db.Float)
    setPressure=db.Column(db.Float)
    seatDiameter=db.Column(db.Float)
    axMeasurement=db.Column(db.Float)
    dnInletUnit=db.Column(db.String(12))
    dnOutletUnit=db.Column(db.String(12))
    setPressureUnit=db.Column(db.String(12))
    createdOn=db.Column(db.DateTime)

    def __init__(self,valve_id,dnInlet,dnOutlet,setPressure,seatDiameter,axMeasurement,dnInletUnit,dnOutletUnit,setPressureUnit):
        self.valve_id=valve_id
        self.dnInletUnit=dnInletUnit
        self.dnInlet=dnInlet
        self.dnOutlet=dnOutlet
        self.dnOutletUnit=dnOutletUnit
        self.setPressure=setPressure
        self.setPressureUnit=setPressureUnit
        self.axMeasurement=axMeasurement
        self.seatDiameter=seatDiameter
        self.createdOn=datetime.now()
    def __repr__(self):
        return '<ValveTD %r>'%self.valve_id

db.create_all()

@app.route('/updateRPSLValveTechData',methods=['POST'])
def updateRPSLValveTechData():
    if request.method=="POST":
        valve_id=request.form.get("valve_id")
        valveTechData=ValveTechincalData.query.filter_by(valve_id=valve_id).first()
        valveTechData.dnInlet=request.form.get('dnInlet')
        valveTechData.dnInletUnit=request.form.get('dnInletUnit')
        valveTechData.dnOutlet=request.form.get('dnOutlet')
        valveTechData.dnOutletUnit=request.form.get('dnOutletUnit')
        valveTechData.setPressure=request.form.get('setPressure')
        valveTechData.seatDiameter=request.form.get('seatDiameter')
        valveTechData.setPressureUnit=request.form.get('setPressureUnit')
        valveTechData.axMeasurement=request.form.get('axMeasurement')
        db.session.commit()
        return jsonify(code=200, message="Updated RPSL valve successfully")

@app.route('/createValve',methods=['POST'])
def createValve():
    if request.method=="POST":
        valve_id=request.form.get('valve_id')
        valve_type=request.form.get('valve_type')
        rev_no=request.form.get('rev_no')
        part_no=request.form.get('part_no')
        install_locations=request.form.get('install_locations')
        customer=request.form.get('customer')
        manufacturer=request.form.get('manufacturer')
        manufacturer_no=request.form.get('manufacturer_no')
        plant=request.form.get('plant')
        valve=Valve(valve_id,valve_type,rev_no,part_no,install_locations,customer,manufacturer,manufacturer_no,plant)
        db.session.add(valve)
        db.session.commit()
        dnInlet=request.form.get('dnInlet')
        dnInletUnit=request.form.get('dnInletUnit')
        dnOutlet=request.form.get('dnOutlet')
        dnOutletUnit=request.form.get('dnOutletUnit')
        setPressure=request.form.get('setPressure')
        setPressureUnit=request.form.get('setPressureUnit')
        seatDiameter=request.form.get('seatDiameter')
        axMeasurement=request.form.get('axMeasurement')
        valveTechData=ValveTechincalData(valve_id,dnInlet,dnOutlet,setPressure,seatDiameter,axMeasurement,dnInletUnit,dnOutletUnit,setPressureUnit)
        db.session.add(valveTechData)
        db.session.commit()
        inspector=request.form.get('inspector')
        testLocation=request.form.get('testLocation')
        testMedium=request.form.get('testMedium')
        applicationNumber=request.form.get('applicationNumber')
        surveyor=request.form.get('surveyor')
        pressureTransducer=request.form.get('pressureTransducer')
        certificationNumber=request.form.get('certificationNumber')
        testDate=datetime.now()
        valveTestData=ValveTestData(valve_id,inspector,testLocation,testMedium,applicationNumber,surveyor,pressureTransducer,certificationNumber,testDate)
        db.session.add(valveTestData)
        db.session.commit()
        return redirect('/showRPSLValves',code=302)
@app.route('/updateRPSLValve',methods=['POST'])
def updateRPSLValve():
    if request.method=="POST":
        valve_id=request.form.get('valve_id')
        valve_type=request.form.get('valve_type')
        rev_no=request.form.get('rev_no')
        part_no=request.form.get('part_no')
        install_locations=request.form.get('install_locations')
        customer=request.form.get('customer')
        manufacturer=request.form.get('manufacturer')
        manufacturer_no=request.form.get('manufacturer_no')
        plant=request.form.get('plant')
        #Get object from db
        valve=Valve.query.filter_by(valve_id=valve_id).first()
        #set values
        valve.valve_type=valve_type
        valve.rev_no=rev_no
        valve.part_no=part_no
        valve.install_locations=install_locations
        valve.customer=customer
        valve.manufacturer=manufacturer
        valve.manufacturer_no=manufacturer_no
        valve.plant=plant
        db.session.commit()
        return jsonify(message="Updated valve data record successfully",code=200)
@app.route("/")
def index():
	return render_template('index.html',current_page="homepage")

@app.route('/showRPSLValves')
def showRPSLValves():
	valves=Valve.query.all()
	return render_template('valves.html',valves=valves,current_page="valves")
@app.route('/deleteRPSLValve',methods=['POST'])
def deleteRPSLValve():
    if request.method=="POST":
        valve_id=request.form.get('valve_id',None)
        valve=Valve.query.filter_by(valve_id=valve_id).first()
        db.session.delete(valve)
        db.session.commit()
        return jsonify(message="Deleted valve successfully!")
@app.route('/valve/<valveNumber>')
def valveCard(valveNumber):
    valveCard=Valve.query.filter_by(valve_id=valveNumber).first()
    valveTechCard=ValveTechincalData.query.filter_by(valve_id=valveNumber).first()
    valveTestCard=ValveTestData.query.filter_by(valve_id=valveNumber).first()
    return render_template('valveCard.html',valveCard=valveCard,current_page="valveCard",valveTechCard=valveTechCard,valveTestCard=valveTestCard)

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
    print process.pid
    pid=process.pid
    process.wait()
    return jsonify(done=200)

@app.route('/showReport',methods=['GET'])
def showReport():
    if request.method=="GET":
        targetPressure=request.args.get('rtargetPressure')
        finalPressure=request.args.get('rfinalPressure')
        actualReleasePressure=request.args.get('ractualPressure')
        valve_id=request.args.get('rvalve_id')
        print targetPressure
        valve=Valve.query.filter_by(valve_id=valve_id).first()
        valveTechCard=ValveTechincalData.query.filter_by(valve_id=valve_id).first()
        valveTestCard=ValveTestData.query.filter_by(valve_id=valve_id).first()
        return render_template('showReport.html',valve=valve,actualReleasePressure=actualReleasePressure,valveTechCard=valveTechCard,valveTestCard=valveTestCard,targetPressure=targetPressure,finalPressure=finalPressure)
    else:
        return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
