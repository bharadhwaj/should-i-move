from flask import Flask, request, render_template, url_for, redirect, flash
from flask.ext.seasurf import SeaSurf #for csrf protection
import requests
import json

app = Flask(__name__)
app.config['DEBUG'] = True
states = [u'Andaman and Nicobar Islands',
 u'ANDHRA PRADESH',
 u'ARUNACHAL PRADESH',
 u'ASSAM',
 u'BIHAR',
 u'CHANDIGARH',
 u'CHHATTISGARH',
 u'Dadra and Nagar Haveli',
 u'Daman and Diu',
 u'DELHI',
 u'GOA',
 u'GUJARAT',
 u'HARYANA',
 u'HIMACHAL PRADESH',
 u'JHARKHAND',
 u'KARNATAKA',
 u'KERALA',
 u'LAKSHADWEEP',
 u'MADHYA PRADESH',
 u'MAHARASHTRA',
 u'MANIPUR',
 u'MEGHALAYA',
 u'MIZORAM',
 u'NAGALAND',
 u'ODISHA',
 u'PUNJAB',
 u'PUDUCHERRY',
 u'RAJASTHAN',
 u'SIKKIM',
 u'TRIPURA',
 u'UTTAR PRADESH',
 u'UTTARAKHAND',
 u'WEST BENGAL']

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'GET':
		return render_template('index.html',states=states)
	elif request.method == 'POST':
		tocity = request.form['toCity']
		fromcity = request.form['fromCity']
		url = "https://ussouthcentral.services.azureml.net/workspaces/6e1d99a68f9f4cf39741814ae82d8221/services/fcb4a576a18e49d68bb854728facf392/execute"

		querystring = {"api-version":"2.0","details":"true","Authorization":"w0nrmDa24icyFTGpIz3i6h73o5466JAD68wkkxPIPWP9ESP4ZCSluLriavMwzHJeDif6nhkOqBYTFBUkGVs8cA=="}

		payload = "{}"
		headers = {
		    'authorization': "Bearer w0nrmDa24icyFTGpIz3i6h73o5466JAD68wkkxPIPWP9ESP4ZCSluLriavMwzHJeDif6nhkOqBYTFBUkGVs8cA==",
		    'content-type': "application/json",
		    'cache-control': "no-cache",
		    'postman-token': "65ff7b39-72f2-8047-8db8-4f8c2ec00f99"
		    }

		response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

	
		result = json.loads(response.text)
		statelist = result["Results"]['output1']['value']['Values']
		statedict = {state:float(score) for state,score in statelist}
		score1 = statedict[fromcity]
		score2 = statedict[tocity]

		diff = abs(score1 - score2) * 100
		print "diff", diff
		text1 = "Yes, You could move from "+fromcity+" to "+tocity+"."
		text2 = "No, It's not safe to move from "+fromcity+" to "+tocity+"."

		print score1, score2
		if score1 < score2:
			text = text1
		else:
			text = text2
		return  render_template('result.html', text=text,tocity=tocity, fromcity=fromcity, score1=score1, score2= score2, diff = diff)


	
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5050)
