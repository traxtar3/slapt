from application import app, db
from flask import render_template, request, json, Response
from application.models import User, Course, Enrollment
from .ceres.getpie import getPIE

courseData = [{"courseID": "1111", "title": "PHP 111", "description": "Intro to PHP", "credits": "3", "term": "Fall, Spring"}, {"courseID": "2222", "title": "Java 1", "description": "Intro to Java Programming", "credits": "4", "term": "Spring"}, {"courseID": "3333", "title": "Adv PHP 201", "description": "Advanced PHP Programming", "credits": "3", "term": "Fall"}, {"courseID": "4444", "title": "Angular 1", "description": "Intro to Angular", "credits": "3", "term": "Fall, Spring"}, {"courseID": "5555", "title": "Java 2", "description": "Advanced Java Programming", "credits": "4", "term": "Fall"}]


from flask import Flask, request, render_template, session, redirect, url_for
from .ceres.sites import BLE, CAV, CLR, COD, EGL, FYL, THL
from .ceres.posneg import PosNegPassToTable  # , get_site_passes
import os

# # tleplace = ˜'/home/johnharms/mysite/tle.txt'
tleplace = '/Users/traxtar3/Dropbox/Coding/Projects/enrollment/application/ceres/tle.txt'


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def adder_page():
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
        # file_ = request.files["myfile"]
        # file_.save('/home/johnharms/mysite/tle.txt') # Save point for TLE file for live sys
            df = PosNegPassToTable(scc, places, hrs, tleplace)
            sccP = df[0].SCC.unique()
            diffx = (list(set(scc) - set(sccP)))

        if scc is not None and hrs is not None and places is not None:
            # return html_string.format(table1=df[0].to_html(classes='mystyle'), table2=df[1].to_html(classes='mystyle'), sccP=str(sccP), diffx=str(diffx))
            # return render_template("slapt.html", login=False)
            return render_template("slapt.html", data={"table1": df[0].to_html(classes='mystyle'), "table2": df[1].to_html(classes='mystyle'), "sccP": str(sccP), "diffx": str(diffx)}, login=True)
            # return render_template("enrollment.html", enrollment=True, data={"id": id, "title": title, "term": term})

    return '''
        <html>
            <body>
                {errors}
                <header class="masthead">
                    <h1>Satellite Look Angle Prediction Tools</h1>
                </header>
                <form method="post" action="." enctype="multipart/form-data">
                    <meta name="viewport" content="width=device-width, initial-scale=1">

                    <!--<p><input type="file" id="myfile" name="myfile"></p>-->

                    <p>Number of hours to forecast from now:
                    <br><input name="hrs" maxlength="2" size="3"/></p>

                    <p><label for="scc">Satellite(s):</label><br><input name="scc" size="100"/>
                    <br>Enter SCCs as comma seperated values (25544, 45589, etc.)

                    <p>Site(s):<br>
                    <select name="place" multiple size="7" style="width: 100px">
                    <option value ="BLE" selected>BLE</option>
                    <option value ="CAV">CAV</option>
                    <option value ="CLR">CLR</option>
                    <option value ="COD">COD</option>
                    <option value ="EGL">EGL</option>
                    <option value ="FYL">FYL</option>
                    <option value ="THL">THL</option>
                    </select>
                    </p>

                    <p><input type="submit" value="Do calculation" style="height:500px; width:500px"/></p>
                </form>


            </body>
            <footer>
            <a href="{license}">License Agreement</a>
            </footer>
        </html>
    '''.format(errors=errors, license=url_for('license'))


@app.route('/license')
def license():
    # return "hello"
    return render_template('License.html')


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


@app.route("/courses/")
@app.route("/courses/<term>")
def courses(term="Spring 2019"):
    return render_template("courses.html", courseData=courseData, courses=True, term=term)


@app.route("/register")
def register():
    return render_template("register.html", register=True)


@app.route("/enrollment", methods=["GET", "POST"])
def enrollment():
    id = request.form.get('courseID')
    title = request.form['title']
    term = request.form.get('term')
    return render_template("enrollment.html", enrollment=True, data={"id": id, "title": title, "term": term})


@app.route("/api/")
@app.route("/api/<idx>")
def api(idx=None):
    if(idx == None):
        jdata = courseData
    else:
        jdata = courseData[int(idx)]

    return Response(json.dumps(jdata), mimetype="application/json")


@app.route("/user")
def user():
    #User(user_id=1, first_name="Christian", last_name="Hur", email="christian@uta.com", password="abc1234").save()
    #User(user_id=2, first_name="Mary", last_name="Jane", email="mary.jane@uta.com", password="password123").save()
    users = User.objects.all()
    return render_template("user.html", users=users)
