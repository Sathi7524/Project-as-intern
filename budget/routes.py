from budget import app,db
from budget.models import workstream,labor_category, project_details,project_budget,budget_breakdown,status_type,user
import os
import pathlib

import requests
from flask import Flask, session, abort, redirect, request,render_template,url_for
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from google.oauth2 import id_token


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "799827868671-g5k0guj84us1klfv9b79ch4cfrmc8bdo.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["picture"]=id_info.get("picture")
    session['family_name']=id_info.get("family_name")
    session['email'] = id_info.get("email")
    print(id_info,session['picture'])
    #us=user(email_id=session['email'],first_name=session['name'],last_name=session['family_name'],role_id=1,status_type=1)
    #db.session.add(us)
    #db.session.commit()
    return redirect("/projects")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/")
def index():
    return render_template('login.html')


@app.route("/protected_area")
@login_is_required
def protected_area():
    return render_template('projects.html')

@app.route('/home')
def home():
    return render_template('home.html')
@app.route("/budget",methods=['GET','POST'])
def budget():
    workst = workstream.query.all()
    labct = labor_category.query.all()
    projects = project_details.query.all()

    return render_template("budget.html",workst=workst,labct=labct,projects=projects,flag=False)

@app.route('/projects',methods=['GET','POST'])
def projects():
    st = status_type.query.all()
    stdic = {}
    for ele in st:
        li = str(ele)[1:-1].split(',')
        stdic[int(li[0])] = str(li[1])[2:-1]

    if request.method=='POST':
        pname=request.form.get('projectname',False)
        cname = request.form.get('clientname', False)
        commdate=request.form.get('commencedate',False)
        dweeks=request.form.get('weeks',False)
        pd=project_details(project_name=pname,client_name=cname,status_flag=1,commence_date=commdate,duration_inweeks=dweeks)
        db.session.add(pd)
        db.session.commit()
    projects= project_details.query.all()
    return render_template('projects.html',projects=projects,stdic=stdic)
@app.route('/allbugets')
def allbudgets():
    return render_template('allbudgets.html')


@app.route('/budget/<id>',methods=['GET','POST'])
def budget_page(id):
    bd = budget_breakdown.query.filter_by(project_budget_id=id).all()
    workst = workstream.query.all()
    workstid2 = {}
    for ele in workst:
        li = str(ele)[1:-1].split(',')
        workstid2[int(li[0])] =str(li[1])[2:-1]

    labct2 = labor_category.query.all()
    labcttype = {}
    labctc = {}
    for ele in labct2:
        li = str(ele)[1:-1].split(',')
        labcttype[int(li[0])] = str(li[1])[2:-1]
        labctc[str(li[1])[2:-1]]=str(li[2])[2:-1]
    labct = labor_category.query.all()
    projects = project_details.query.all()
    if request.method=='POST':
        projectidname=request.form.get('projectidname')
        workst1=request.form.get('workstream', False)
        labor=request.form.get('labor_category', False)
        hours=request.form.get('totallaborhours', False)
        cost=request.form.get('costperhour', False)
        ct=request.form.get('country',False)
        projectdid=request.form.get('project_details_id', False)
        workstid=workstream.query.filter_by(name=workst1).first().workstream_id
        labctid=labor_category.query.filter_by(labor_type=labor,country=ct).first().labor_id
        bd=budget_breakdown(project_budget_id=id,labor_category_id=labctid,labor_hours=hours,workstream_id=workstid,pay_per_hour=cost)
        db.session.add(bd)
        db.session.commit()
        bd=budget_breakdown.query.filter_by(project_budget_id=id).all()

        return render_template("budget_page.html",id=id,bd=bd,workst=workst,labct=labct,projects=projects,workstid=workstid,workst1=workst1,labor=labor,hours=int(hours),ct=ct,cost=int(cost),workstid2=workstid2,labcttype=labcttype,labctc=labctc,flag=True)

    return render_template('budget_page.html',id=id,bd=bd,workst=workst,labct=labct,projects=projects,workstid2=workstid2,labcttype=labcttype,labctc=labctc)


@app.route('/delete/<id>',methods=['GET','POST'])
def delete(id):
    bd = budget_breakdown.query.filter_by(budget_breakdown_id=id).first()
    bd1=bd
    print(request.referrer)
    if request.method=='POST':
        budget_breakdown1 =budget_breakdown.query.filter_by(budget_breakdown_id=id).delete()
        db.session.commit()
        #return redirect(f'/budget/{bd}')
    return redirect(request.referrer)

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/manageworkstream',methods=['GET','POST'])
def manageworkstream():
    if request.method=='POST':
        wstname=request.form.get('name',False)
        wt = workstream(name=wstname)
        db.session.add(wt)
        db.session.commit()
    workst = workstream.query.all()
    workstid2 = {}
    for ele in workst:
        li = str(ele)[1:-1].split(',')
        workstid2[int(li[0])] = str(li[1])[2:-1]

    return render_template('manageworkstream.html',workstid2=workstid2)


@app.route('/managelabor',methods=['GET','POST'])
def managelabor():
    if request.method=='POST':
        ltype = request.form.get('labortype', False)
        lc = request.form.get('Country', False)
        lcost=int(request.form.get('cost',False))
        wt = labor_category(type=ltype,country=lc,cost=lcost)
        db.session.add(wt)
        db.session.commit()
    labct2 = labor_category.query.all()
    labcttype = {}
    labctc = {}
    labctcost = {}
    for ele in labct2:
        li = str(ele)[1:-1].split(',')
        labcttype[int(li[0])] = str(li[1])[2:-1]
        labctc[int(li[0])] = str(li[2])[2:-1]
        labctcost[int(li[0])] = float(li[3])

    return render_template('managelabor.html',labcttype=labcttype,labctc=labctc,labctcost=labctcost)

@app.route('/manageusers')
def manageusers():
    us = user.query.all()
    l = []
    for ele in us:
        li = str(ele)[1:-1].split(',')
        li[0] = int(str(li[0]))
        li[1] = str(li[1])[2:-1]
        li[2] = str(li[2])[2:-1]
        li[3] = str(li[3])[2:-1]
        l.append(li)

    return render_template('manageusers.html',users=l)





