from flask import Flask,render_template,url_for
from flask import request, session, g, redirect, abort, flash,jsonify
import os
import subprocess
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,static_folder='static',static_url_path='/static')
app.secret_key = os.urandom(24)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////efco.db'
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
    seatPressure=db.Column(db.Float)
    seatDiameter=db.Column(db.Float)
    axMeasurement=db.Column(db.Float)
    dnInletUnit=db.Column(db.String(12))
    dnOutletUnit=db.Column(db.String(12))
    seatPressureUnit=db.Column(db.String(12))
    createdOn=db.Column(db.DateTime)

    def __init__(self,valve_id,dnInlet,dnOutlet,seatPressure,seatDiameter,axMeasurement,dnInletUnit,dnOutletUnit,seatPressureUnit):
        self.valve_id=valve_id
        self.dnInletUnit=dnInletUnit
        self.dnInlet=dnInlet
        self.dnOutlet=dnOutlet
        self.dnOutletUnit=dnOutletUnit
        self.seatPressure=seatPressure
        self.seatPressureUnit=seatPressureUnit
        self.axMeasurement=axMeasurement
        self.seatDiameter=seatDiameter
        self.createdOn=datetime.now()
    def __repr__(self):
        return '<ValveTD %r>'%self.valve_id

class CertificationNumber(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    date=db.Column(db.String(8))
    count=db.Column(db.Integer)

    def __init__(self,date,count):
        self.date=date
        self.count=count
    def __repr__(self):
        return '<CertificationNumber %r>'%self.date+str(self.count)

# class ValveTestReport(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     valve_id = db.Column(db.Integer, db.ForeignKey(Valve))

db.create_all()

def save(data):
    db.session.add(data)
    db.session.commit()

@app.route("/")
def index():
    timedata=str(datetime.now().date())
    timedata=timedata.replace("-","")
    certnum=CertificationNumber.query.filter_by(date=timedata).first()
    if certnum is None:
        certnum=CertificationNumber(timedata,0)
        db.session.add(certnum)
        db.session.commit()
    return render_template('index.html',current_page="homepage")

def generateCertificationNumber():
    timedata=str(datetime.now().date())
    timedata=timedata.replace("-","")
    certnum=CertificationNumber.query.filter_by(date=timedata).first()
    certnum.count=int(certnum.count)+1
    save(certnum)
    return certnum.date+str(certnum.count)

@app.route('/updateRPSLValveTechData',methods=['POST'])
def updateRPSLValveTechData():
    if request.method=="POST":
        valve_id=request.form.get("valve_id")
        valveTechData=ValveTechincalData.query.filter_by(valve_id=valve_id).first()
        valveTechData.dnInlet=request.form.get('dnInlet')
        valveTechData.dnInletUnit=request.form.get('dnInletUnit')
        valveTechData.dnOutlet=request.form.get('dnOutlet')
        valveTechData.dnOutletUnit=request.form.get('dnOutletUnit')
        valveTechData.seatPressure=request.form.get('seatPressure')
        valveTechData.seatDiameter=request.form.get('seatDiameter')
        valveTechData.seatPressureUnit=request.form.get('seatPressureUnit')
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
        save(valve)
        dnInlet=request.form.get('dnInlet')
        dnInletUnit=request.form.get('dnInletUnit')
        dnOutlet=request.form.get('dnOutlet')
        dnOutletUnit=request.form.get('dnOutletUnit')
        seatPressure=request.form.get('seatPressure')
        seatPressureUnit=request.form.get('seatPressureUnit')
        seatDiameter=request.form.get('seatDiameter')
        axMeasurement=request.form.get('axMeasurement')
        valve_created=Valve.query.filter_by(valve_id=valve_id,valve_type=valve_type).first()
        valveTechData=ValveTechincalData(valve_created.id,dnInlet,dnOutlet,seatPressure,seatDiameter,axMeasurement,dnInletUnit,dnOutletUnit,seatPressureUnit)
        save(valveTechData)
        inspector=request.form.get('inspector')
        testLocation=request.form.get('testLocation')
        testMedium=request.form.get('testMedium')
        applicationNumber=request.form.get('applicationNumber')
        surveyor=request.form.get('surveyor')
        pressureTransducer=request.form.get('pressureTransducer')
        certificationNumber=request.form.get('certificationNumber')
        testDate=datetime.now()
        valveTestData=ValveTestData(valve_created.id,inspector,testLocation,testMedium,applicationNumber,surveyor,pressureTransducer,certificationNumber,testDate)
        save(valveTestData)
        requested_page=request.form.get('current_page')
        if requested_page=="RPSLvalves":
            return redirect('/showRPSLValves',code=302)
        elif requested_page=="BTSLvalves":
            return redirect('/showBTSLValves',code=302)
        else:
            return redirect('/',code=302)
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

@app.route('/showRPSLValves')
def showRPSLValves():
    """Shows all valves of type = 1 (`Safety Valve`)"""
    valves=Valve.query.filter_by(valve_type=1).all()
    return render_template('valves.html',valves=valves,current_page="RPSLvalves")

@app.route('/showBTSLValves')
def showBTSLValves():
    """Shows all valves of type = 2 (`Shut off Valve`)"""
    valves=Valve.query.filter_by(valve_type=2).all()
    return render_template('valves.html',valves=valves,current_page="BTSLvalves")

@app.route('/deleteValve/<valve_id>/<valve_type>')
def deleteValve(valve_id,valve_type):
    valve=Valve.query.filter_by(valve_id=valve_id,valve_type=valve_type).first()
    valveTechCard=ValveTechincalData.query.filter_by(valve_id=valve.id).first()
    valveTestCard=ValveTestData.query.filter_by(valve_id=valve.id).first()
    db.session.delete(valve)
    db.session.delete(valveTechCard)
    db.session.delete(valveTestCard)
    db.session.commit()
    if valve_type=="1":
        return redirect('/showRPSLValves',code=302)
    elif valve_type=="2":
        return redirect('/showBTSLValves',code=302)
    else:
        return redirect('/',code=302)

@app.route('/rpslvalve/<valveNumber>')
def rpslValveCard(valveNumber):
    valveCard=Valve.query.filter_by(valve_id=valveNumber,valve_type=1).first()
    valveTechCard=ValveTechincalData.query.filter_by(valve_id=valveCard.id).first()
    valveTestCard=ValveTestData.query.filter_by(valve_id=valveCard.id).first()
    timedata=str(datetime.now().date())
    timedata=timedata.replace("-","")
    certnum=CertificationNumber.query.filter_by(date=timedata).first()
    certnum=str(certnum.date)+str("%03d"%(certnum.count+1,))
    return render_template('rpslValveCard.html',certnum=certnum,valveCard=valveCard,current_page="valveCard",valveTechCard=valveTechCard,valveTestCard=valveTestCard)

@app.route('/btslvalve/<valveNumber>')
def btslValveCard(valveNumber):
    valveCard=Valve.query.filter_by(valve_id=valveNumber,valve_type=2).first()
    valveTechCard=ValveTechincalData.query.filter_by(valve_id=valveCard.id).first()
    valveTestCard=ValveTestData.query.filter_by(valve_id=valveCard.id).first()
    timedata=str(datetime.now().date())
    timedata=timedata.replace("-","")
    certnum=CertificationNumber.query.filter_by(date=timedata).first()
    certnum=str(certnum.date)+str("%03d"%(certnum.count+1,))
    return render_template('btslValveCard.html',certnum=certnum,valveCard=valveCard,current_page="btslvalveCard",valveTechCard=valveTechCard,valveTestCard=valveTestCard)

@app.route('/startRPVI',methods=['GET'])
def startRPVI():
    command='C:\\Users\\user\\Documents\\builds\\EfcoDAQ\\releasePressure\\releasePressure.exe'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    print process.returncode
    return jsonify(done=200,status_code=200)

@app.route('/startSLVI',methods=['GET'])
def startSLVI():

    command='C:\\Users\\user\\Documents\\builds\EfcoDAQ\\seatLeakage\\seatLeakage.exe'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    pid=process.pid
    process.wait()
    return jsonify(status_code=200,done=200)

@app.route('/startBTVI',methods=['GET'])
def startBTVI():
    command='C:\\Users\\user\\Documents\\builds\EfcoDAQ\\bodyTest\\bodyTest.exe'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    pid=process.pid
    process.wait()
    return jsonify(status_code=200,done=200)

@app.route('/showReport',methods=['GET'])
def showReport():
    if request.method=="GET":
        targetPressure=request.args.get('rtargetPressure')
        finalPressure=request.args.get('rfinalPressure')
        actualReleasePressure=request.args.get('ractualPressure')
        valve_id=request.args.get('rvalve_id')
        valve_type=request.args.get('valve_type')
        valve=Valve.query.filter_by(valve_id=valve_id,valve_type=valve_type).first()
        valveTechCard=ValveTechincalData.query.filter_by(valve_id=valve.id).first()
        valveTestCard=ValveTestData.query.filter_by(valve_id=valve.id).first()
        print valveTestCard
        return render_template('showReport.html',valve=valve,actualReleasePressure=actualReleasePressure,valveTechCard=valveTechCard,valveTestCard=valveTestCard,targetPressure=targetPressure,finalPressure=finalPressure)
    else:
        return redirect('/')

@app.route('/faq')
def faq():
    return render_template('faq.html')

if __name__ == "__main__":
    app.run(debug=True,port=80)
