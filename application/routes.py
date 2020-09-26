from application import app
from flask import render_template, request, json, Response, current_app
from .ceres.getpie import getPIE
from pathlib import Path
import pandas as pd
from datetime import datetime
from .ceres.sandbox import mkTaskData
from flask import Flask, request, render_template, session, redirect, url_for
from .ceres.sites import BLE, CAV, CLR, COD, EGL, FYL, THL
from .ceres.posneg import PosNegPassToTable  # , get_site_passes
import os

from .poca.poca import getRSS, getTime
from .poca.util import convertTLE, twobody2, jsattime, inverseDt

# # tleplace = '/home/johnharms/slapt/application/ceres/tle.txt'
# tleplace = '/Users/traxtar3/Dropbox/Coding/Projects/slapt/v20200529/application/ceres/tle.txt'
tleplace = 'application/ceres/tle.txt'


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
# @app.route("/home", methods=["GET", "POST"])
def index():
    errors = ""
    if request.method == "POST":
        scc = None
        hrs = None
        try:
            hrs = float(request.form["hrs"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["hrs"])
        try:
            hrs = float(request.form["hrs"]) < 100
        except:
            errors += "<p>{!r} is greater than 100.</p>\n".format(request.form["hrs"])

        hrs = int(request.form["hrs"])
        scc = list(request.form["scc"].split(","))
        for i in range(0, len(scc)):
            scc[i] = int(scc[i])
        scc = set(scc)
        places = request.form.getlist('place')
        for n, i in enumerate(places):
            if i == 'BLE':
                places[n] = BLE
            if i == 'CAV':
                places[n] = CAV
            if i == 'CLR':
                places[n] = CLR
            if i == 'COD':
                places[n] = COD
            if i == 'EGL':
                places[n] = EGL
            if i == 'FYL':
                places[n] = FYL
            if i == 'THL':
                places[n] = THL
        # print(places)
        # file_ = request.files["myfile"]
        # file_.save('/home/johnharms/mysite/tle.txt') # Save point for TLE file for live sys
        df = PosNegPassToTable(scc, places, hrs, tleplace)
        sccP = df[0].SCC.unique()
        diffx = (list(set(scc) - set(sccP)))

        if scc is not None and hrs is not None and places is not None:
            # return html_string.format(table1=df[0].to_html(classes='mystyle'), table2=df[1].to_html(classes='mystyle'), sccP=str(sccP), diffx=str(diffx))
            # return render_template("slapt.html", login=False)
            return render_template("slapt.html", data={"table1": df[0].to_html(classes='mystyle'), "table2": df[1].to_html(classes='mystyle'), "sccP": str(sccP), "diffx": str(diffx)}, index=True)
            # return render_template("enrollment.html", enrollment=True, data={"id": id, "title": title, "term": term})

    return render_template("index.html", index=True)


@app.route('/license')
def license():
    # return "hello"
    return render_template('License.html')


@app.route("/poca", methods=["GET", "POST"])
def poca():
    errors = ""
    if request.method == "POST":
        pocascc1 = None
        pocascc2 = None
        pocahrs = None
        poactol = None
        try:
            hrs = float(request.form["pocahrs"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["pocahrs"])
        try:
            hrs = float(request.form["pocahrs"]) < 72
        except:
            errors += "<p>{!r} is greater than 72.</p>\n".format(request.form["pocahrs"])

        pocahrs = int(request.form["pocahrs"])
        pocascc1 = str(request.form["pocascc1"])
        pocascc2 = str(request.form["pocascc2"])
        pocatol = int(request.form["pocatol"])

        pocaout = getRSS(pocascc1, pocascc2, pocahrs, 120, pocatol, tleplace)

        age1 = datetime.utcnow() - getTime(pocascc1, tleplace)
        age2 = datetime.utcnow() - getTime(pocascc2, tleplace)

        if pocascc1 is not None and pocascc2 is not None and pocahrs is not None:
            # if 'form2-submit' in request.form:
            # return html_string.format(table1=df[0].to_html(classes='mystyle'), table2=df[1].to_html(classes='mystyle'), sccP=str(sccP), diffx=str(diffx))
            # return render_template("slapt.html", login=False)
            return render_template("pocaout.html", data={"table1": pocaout.to_html(classes='mystyle'), "age1": age1, "age2": age2, "pocascc1": pocascc1, "pocascc2": pocascc2}, poca=True)
            # return render_template("enrollment.html", enrollment=True, data={"id": id, "title": title, "term": term})

    return render_template("pocain.html", poca=True)


# @app.route("/enrollment", methods=["GET", "POST"])
# def slapt():
#     id = request.form.get('courseID')
#     title = request.form['title']
#     term = request.form.get('term')
#     return render_template("enrollment.html", enrollment=True, data={"id": id, "title": title, "term": term})


# @app.route("/")
# @app.route("/index")
# @app.route("/home")
# def index():
#     return render_template("index.html", index=True)


@app.route("/login")
def login():
    return render_template("login.html", login=True)


@app.route("/taskings/")
@app.route("/taskings/<site>")
def taskings():
    taskData = mkTaskData()
    return render_template("taskings.html", data={"table1": taskData.to_html(classes='mystyle')}, taskings=True)


@app.route("/register")
def register():
    return render_template("register.html", register=True)


@app.route("/voicereport")
def voicereport():
    return render_template("voicereport.html", voicereport=True)


@app.route("/ble_taskings")
def ble_taskings():
    taskData = mkTaskData()
    taskDataBLE = taskData[taskData['Site'] == 'BLE']
    return render_template("taskings/ble_taskings.html", data={"table1": taskDataBLE.to_html(classes='mystyle')})


@app.route("/cav_taskings")
def cav_taskings():
    taskData = mkTaskData()
    taskDataCAV = taskData[taskData['Site'] == 'CAV']
    return render_template("taskings/cav_taskings.html", data={"table1": taskDataCAV.to_html(classes='mystyle')})


@app.route("/clr_taskings")
def clr_taskings():
    taskData = mkTaskData()
    taskDataCLR = taskData[taskData['Site'] == 'CLR']

    return render_template("taskings/clr_taskings.html", data={"table1": taskDataCLR.to_html(classes='mystyle')})


@app.route("/cod_taskings")
def cod_taskings():
    taskData = mkTaskData()
    taskDataCOD = taskData[taskData['Site'] == 'COD']
    return render_template("taskings/cod_taskings.html", data={"table1": taskDataCOD.to_html(classes='mystyle')})


@app.route("/egl_taskings")
def egl_taskings():
    taskData = mkTaskData()
    taskDataEGL = taskData[taskData['Site'] == 'EGL']
    return render_template("taskings/egl_taskings.html", data={"table1": taskDataEGL.to_html(classes='mystyle')})


@app.route("/fyl_taskings")
def fyl_taskings():
    taskData = mkTaskData()
    taskDataFYL = taskData[taskData['Site'] == 'FYL']
    return render_template("taskings/fyl_taskings.html", data={"table1": taskDataFYL.to_html(classes='mystyle')})


@app.route("/thl_taskings")
def thl_taskings():
    taskData = mkTaskData()
    taskDataTHL = taskData[taskData['Site'] == 'THL']
    return render_template("taskings/thl_taskings.html", data={"table1": taskDataTHL.to_html(classes='mystyle')})


# @app.route("/enrollment", methods=["GET", "POST"])
# def enrollment():
#     id = request.form.get('courseID')
#     title = request.form['title']
#     term = request.form.get('term')
#     return render_template("enrollment.html", enrollment=True, data={"id": id, "title": title, "term": term})


# @app.route("/api/")
# @app.route("/api/<idx>")
# def api(idx=None):
#     if(idx == None):
#         jdata = courseData
#     else:
#         jdata = courseData[int(idx)]

#     return Response(json.dumps(jdata), mimetype="application/json")


# @app.route("/user")
# def user():
#     # User(user_id=1, first_name="Christian", last_name="Hur", email="christian@uta.com", password="abc1234").save()
#     # User(user_id=2, first_name="Mary", last_name="Jane", email="mary.jane@uta.com", password="password123").save()
#     users = User.objects.all()
#     return render_template("user.html", users=users)

    # return render_template("index.html", index=True)
