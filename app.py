from flask import Flask, render_template, session, json, request, redirect
from flask_mysqldb import MySQL
from google.cloud import translate_v2 as translate
import google.auth
from google.oauth2 import service_account

app = Flask(__name__)
app.config["SECRET_KEY"] = "ShuJAxtrE8tO5ZT"

# MySQL configurations
app.config['MYSQL_USER'] = 'abrenon'
app.config['MYSQL_PASSWORD'] = 'anywheremysql'
app.config['MYSQL_DB'] = 'abrenon$workspace'
app.config['MYSQL_HOST'] = 'abrenon.mysql.pythonanywhere-services.com'
mysql = MySQL(app)

credentials = service_account.Credentials.from_service_account_file("/home/abrenon/My Project-1f2512d178cb.json")
translate_client = translate.Client(credentials=credentials)

romans = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]

@app.route("/")
def index():
	reg = ins = prop = room = arc = gdoc = ""

	if (session.get('region')):
		reg = session['region']
	if (session.get('insula')):
		ins = session['insula']
	if (session.get('property')):
		prop = session['property']
	if (session.get('room')):
		room = session['room']
	if (session.get('arc')):
		arc = session['arc']
	if (session.get('gdoc')):
		gdoc = session['gdoc']


	return render_template('index.html',
		region=reg, insula=ins, property=prop, room=room,
		gdoc=gdoc, arc=arc)

@app.route("/PPP")
def showPPP():

	pppCur = mysql.connection.cursor()
	pppQuery = "SELECT id, description FROM PPP WHERE location LIKE %s;"
	loc = ""
	if (session.get('region')):
		loc += session['region']
	if (session.get('insula')):
		loc += session['insula']
	if (session.get('property')):
		loc += session['property']
	if (session.get('room')):
		loc += session['room']

	if loc != "":
		loc += "%"

	pppCur.execute(pppQuery, [loc])
	data = pppCur.fetchall()
	pppCur.close()

	indices = []
	for d in data:
		indices.append(d[0])

	transdata = []
	for d in data:
		translation = translate_client.translate(d[1], target_language="en", source_language="it")
		transdata.append(translation['translatedText'])

	ppp = reg = ins = prop = room = ""

	if (session.get('region')):
		reg = session['region']
	if (session.get('insula')):
		ins = session['insula']
	if (session.get('property')):
		prop = session['property']
	if (session.get('room')):
		room = session['room']

	if (session.get('carryoverPPP')):
		ppp = session['carryoverPPP']

	return render_template('PPP.html',
		catextppp=ppp, dbdata = data, transdata = transdata, indices = indices,
		region=reg, insula=ins, property=prop, room=room)

@app.route('/PPM')
def showPPM():

	ppmCur = mysql.connection.cursor()
	ppmQuery = "SELECT id, description FROM PPM WHERE location LIKE %s;"
	loc = ""
	if (session.get('region')):
		romin = int(session['region']) - 1
		if romin >= 0 and romin < len(romans):
			romreg = romans[romin]
			loc += romreg
	if (session.get('insula')):
		loc += session['insula']
	if (session.get('property')):
		loc += session['property']
	if (session.get('room')):
		loc += session['room']

	if loc != "":
		loc += "%"

	ppmCur.execute(ppmQuery, [loc])
	data = ppmCur.fetchall()
	ppmCur.close()

	indices = []
	for d in data:
		indices.append(d[0])

	transdata = [] #
	dataplustrans = []
	for d in data:
		translation = translate_client.translate(d[1], target_language="en", source_language="it")
		transdata.append(translation['translatedText'])
		dlist = list(d)
		dlist.append(translation['translatedText'])
		dataplustrans.append(dlist)

	ppm = ppmimg = reg = ins = prop = room = ""

	if (session.get('region')):
		reg = session['region']
	if (session.get('insula')):
		ins = session['insula']
	if (session.get('property')):
		prop = session['property']
	if (session.get('room')):
		room = session['room']

	if (session.get('carryoverPPM')):
		ppm = session['carryoverPPM']
	if (session.get('carryoverPPMImgs')):
		ppmimg = session['carryoverPPMImgs']

	return render_template('PPM.html',
		catextppm=ppm, catextppmimg=ppmimg, dbdata = dataplustrans, transdata = transdata, indices = indices,
		region=reg, insula=ins, property=prop, room=room)

@app.route('/ppm-reviewed')
def ppmReviewed():
	strargs = request.args['data'].replace("[", "").replace("]", "")
	ppmCur = mysql.connection.cursor()
	ppmQuery = "UPDATE PPM SET reviewed=1 WHERE id in (" + strargs + ") ;"
	ppmCur.execute(ppmQuery)
	mysql.connection.commit()
	ppmCur.close()

	return redirect('/PPM')

@app.route('/ppp-reviewed')
def pppReviewed():
	strargs = request.args['data'].replace("[", "").replace("]", "")
	pppCur = mysql.connection.cursor()
	pppQuery = "UPDATE PPP SET reviewed=1 WHERE id in (" + strargs + ") ;"
	pppCur.execute(pppQuery)
	mysql.connection.commit()
	pppCur.close()

	return redirect('/PPP')


@app.route('/PinP')
def showPinP():
	pinp = reg = ins = prop = room = ""

	if (session.get('region')):
		reg = session['region']
	if (session.get('insula')):
		ins = session['insula']
	if (session.get('property')):
		prop = session['property']
	if (session.get('room')):
		room = session['room']

	if (session.get('carryoverPinP')):
		pinp = session['carryoverPinP']
	return render_template('PinP.html',
		catextpinp=pinp, 
		region=reg, insula=ins, property=prop, room=room)

@app.route('/help')
def help():
	reg = ins = prop = room = ""

	if (session.get('region')):
		reg = session['region']
	if (session.get('insula')):
		ins = session['insula']
	if (session.get('property')):
		prop = session['property']
	if (session.get('room')):
		room = session['room']

	return render_template('help.html',
		region=reg, insula=ins, property=prop, room=room)

@app.route('/GIS')
def GIS():
	reg = ins = prop = room = ""

	if (session.get('region')):
		reg = session['region']
	if (session.get('insula')):
		ins = session['insula']
	if (session.get('property')):
		prop = session['property']
	if (session.get('room')):
		room = session['room']

	return render_template('GIS.html',
		region=reg, insula=ins, property=prop, room=room)


@app.route('/descriptions')
def showDescs():
	ppp = ppm = ppmimg = pinp = reg = ins = prop = room = gdoc = ""

	if (session.get('region')):
		reg = session['region']
	if (session.get('insula')):
		ins = session['insula']
	if (session.get('property')):
		prop = session['property']
	if (session.get('room')):
		room = session['room']

	if (session.get('carryoverPPP')):
		ppp = session['carryoverPPP']
	if (session.get('carryoverPPM')):
		ppm = session['carryoverPPM']
	if (session.get('carryoverPPMImgs')):
		ppmimg = session['carryoverPPMImgs']
	if (session.get('carryoverPinP')):
		pinp = session['carryoverPinP']

	if (session.get('gdoc')):
		gdoc = session['gdoc']

	return render_template('descs.html',
		carryoverPPP=ppp, carryoverPPM=ppm, carryoverPPMImgs=ppmimg, carryoverPinP=pinp,
		region=reg, insula=ins, property=prop, room=room, gdoc=gdoc)

@app.route('/carryover', methods=['POST'])
def carryover_text():
	if (request.form.get('catextppp')):
		session['carryoverPPP'] = request.form['catextppp']
	if (request.form.get('catextppm')):
		session['carryoverPPM'] = request.form['catextppm']
	if (request.form.get('catextppmimg')):
		session['carryoverPPMImgs'] = request.form['catextppmimg']
	if (request.form.get('catextpinp')):
		session['carryoverPinP'] = request.form['catextpinp']
	return redirect(request.referrer)

@app.route('/carryover-button')
def carryover_button():
	if (request.args.get('catextppp')):
		session['carryoverPPP'] = request.args['catextppp']
	if (request.args.get('catextppm')):
		session['carryoverPPM'] = request.args['catextppm']
	if (request.args.get('catextppmimg')):
		session['carryoverPPMImgs'] = request.args['catextppmimg']
	if (request.args.get('catextpinp')):
		session['carryoverPinP'] = request.args['catextpinp']
	return redirect(request.referrer)

@app.route('/cleardata')
def clearData():
	session['carryoverPPP'] = ""
	session['carryoverPPM'] = ""
	session['carryoverPPMImgs'] = ""
	session['carryoverPinP'] = ""

	session['arc'] = ""
	session['region'] = ""
	session['insula'] = ""
	session['property'] = ""
	session['room'] = ""

	session['gdoc'] = ""

	return render_template('index.html')

@app.route('/savedata')
def saveData():

	cur = mysql.connection.cursor()
	saveQuery = """INSERT INTO FinalData(ARC, Region, Insula, Property, Room, PPM, PPP, PPMImgs, PinP)
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
		ON DUPLICATE KEY UPDATE
		Region = VALUES(Region),
		Insula = VALUES(Insula),
		Property = VALUES(Property),
		Room = VALUES(Room),
		PPM = VALUES(PPM),
		PPP = VALUES(PPP),
		PPMImgs = VALUES(PPMImgs),
		PinP = VALUES(PinP);"""

	queryvars = [session['arc']]
	if (session.get('region')):
		queryvars.append(session['region'])
	else:
		queryvars.append("")
	if (session.get('insula')):
		queryvars.append(session['insula'])
	else:
		queryvars.append("")
	if (session.get('property')):
		queryvars.append(session['property'])
	else:
		queryvars.append("")
	if (session.get('room')):
		queryvars.append(session['room'])
	else:
		queryvars.append("")


	if (session.get('carryoverPPP')):
		queryvars.append(session['carryoverPPP'])
	else:
		queryvars.append("")
	if (session.get('carryoverPPM')):
		queryvars.append(session['carryoverPPM'])
	else:
		queryvars.append("")
	if (session.get('carryoverPPMImgs')):
		queryvars.append(session['carryoverPPMImgs'])
	else:
		queryvars.append("")
	if (session.get('carryoverPinP')):
		queryvars.append(session['carryoverPinP'])
	else:
		queryvars.append("")


	cur.execute(saveQuery, queryvars)
	mysql.connection.commit()
	cur.close()

	return redirect(request.referrer)

@app.route('/search', methods=['POST'])
def search():
	if (request.form.get('region')):
		session['region'] = request.form['region']
	if (request.form.get('insula')):
		session['insula'] = request.form['insula']
	if (request.form.get('property')):
		session['property'] = request.form['property']
	if (request.form.get('room')):
		session['room'] = request.form['room']
	return redirect(request.referrer)

@app.route('/init', methods=['POST'])
def init():
	session['arc'] = request.form['arc']
	session['gdoc'] = request.form['gdoc']
	if (request.form.get('region')):
		session['region'] = request.form['region']
	if (request.form.get('insula')):
		session['insula'] = request.form['insula']
	if (request.form.get('property')):
		session['property'] = request.form['property']
	if (request.form.get('room')):
		session['room'] = request.form['room']
	return redirect('/PPP')


if __name__ == "__main__":
	app.run()