import os
import datetime
import flask
import json
import werkzeug

import getRosterHtml
import makeRosterImg

app = flask.Flask(__name__)

MAX_AGE_MIN = 10.  # Maximum age that an image will have before being re-generated.

@app.route("/")
def hello():
    #return "Hello World from parkrun tokens web app"
    return flask.redirect("/static/index.html", code=302)

#@app.route("/refresh", methods=['GET', 'POST'])
def refreshRoster():
    ''' Attempt to refresh the stored roster image for the requested parkrun.
    Returns True on success or False if it fails.
    '''
    print(flask.request.values)
    prNameTxt = flask.request.values.get('pRunName')
    if prNameTxt is None:
        prNameTxt = "hartlepool"
    dataTxt = flask.request.data.decode("utf-8")
    print("prNameTxt=",prNameTxt)
    fname = "dynamic/roster_%s.png" % prNameTxt

    # Generate a new roster dashboard
    htmlStr = getRosterHtml.getRosterHtml(prNameTxt, debug=False)
    if (htmlStr is None):
        print("Error Reading Roster from Parkrun Website")
        return False
    rosterData = makeRosterImg.getRosterData(htmlStr,columnNo=0,debug=False)
    makeRosterImg.makeDashboardImage(rosterData,"png", fname, debug=False)
    return True

@app.route("/get", methods=['GET', 'POST'])
def getRoster():
    print(flask.request.values)
    prNameTxt = flask.request.values.get('pRunName')
    if prNameTxt is None:
        prNameTxt = "hartlepool"
    dataTxt = flask.request.data.decode("utf-8")
    print("prNameTxt=",prNameTxt)
    fname = "dynamic/roster_%s.png" % prNameTxt

    if not os.path.exists(fname):
        print("No cached version of roster - generating new one")
        if refreshRoster():
            return flask.send_file(fname)
        else:
            return("Error generating roster image")
    else:
        print("File %s exists - checking its age..." % fname)

    fnameAge = (datetime.datetime.today() - datetime.datetime.fromtimestamp(os.path.getmtime(fname))).total_seconds()
    print("fname=%s, age=%.1f min" % (fname, fnameAge/60.))

    if (fnameAge > MAX_AGE_MIN*60.):
        print("Image is too old - re-generating")
        if refreshRoster():
            return flask.send_file(fname)
        else:
            return("Error generating roster image")
    else:
        print("Image age OK")
    return flask.send_file(fname)


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=8080)
