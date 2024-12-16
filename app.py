from flask import Flask,render_template,request,redirect
from pymongo import MongoClient

client=MongoClient("localhost",27017)
db=client["userdetails"]
u_details=db["u_details"]
u_login=db["u_login"]
u_payment=db["u_payment"]
merchent=db["merchent"]
maincredit={"CREDIT":0}

app=Flask(__name__)

@app.route("/",methods=["GET"])
def homepage():
    return render_template("index.html")
@app.route("/user",methods=["GET"])
def user():
    return render_template("user.html")
@app.route("/user_register",methods=["GET","POST"])
def userreg():
    if request.method=="POST":
        iD=int(request.form["id"])
        name=request.form["name"]
        email=request.form["email"]
        password=request.form["password"]
        phone=request.form["phone"]
        address=request.form["address"]
        credit=int(request.form["credit"])
        maincredit["CREDIT"]=credit
        u_details.insert_one({
            "USER_ID":iD,"U_NAME":name,"U_EMAIL":email,"PASSWORD":password,"U_PHONE":phone,"U_ADDRESS":address,"CREDIT_AMOUNT":credit
        })
        return redirect("/user_register")
    else:
        return render_template("/user_register.html")
@app.route("/userlogin",methods=["GET","POST"])
def userlogin():

    if request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]
        u_login.insert_one({
            "U_EMAIL":email,"PASSWORD":password
        })
        return redirect("/pay")
    else:
        return render_template("/user_login.html")

@app.route("/merchentr",methods=["GET","POST"])
def mer_reg():
    if request.method=="POST":
        Id=int(request.form["id"])
        App=request.form["App"]
        transaction=int(request.form["transaction"])
        merchent.insert_one({
            "MER_ID":Id,"M_APP":App,"M_TRANSACTION":transaction
        })
        return redirect("/merchentr")
    else:
        return render_template("merchentr.html")
@app.route("/pay",methods=["GET","POST"])
def payment():
    if request.method=="POST":
        email=request.form["email"]
        App=request.form["App"]
        Item=(request.form["item"])
        Amount=int(request.form["amount"])
        upmaincredit=abs(maincredit["CREDIT"]-Amount)
        u_details.update_one({"email":email},{"$set":{"CREDIT":upmaincredit}})
        u_payment.insert_one({
            "email":email,"APP":App,"ITEM":Item,"Amount":Amount
        })
        return redirect("/pay")
    else:
        return render_template("payment.html")
@app.route("/user_due",methods=["GET","POST"])
def userdue():
    u_details.find()
    return render_template("userdetails.html")


app.run(debug=True)
        