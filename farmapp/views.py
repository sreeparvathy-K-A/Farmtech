from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import *
# import MySQLdb
from .models import Registration, Login, Addcropdetails, Addnews
from django.contrib import messages
from django.db import connection
from django.db.models import Q, Max, Count

# con=MySQLdb.connect("localhost","root","","farmer")
# c=con.cursor()
# Create your views here.


def index(request):
    return render(request, "index.html")


def contact(request):
    return render(request, "contact.html")


def common(request):
    return render(request, "common.html")


def UserHome(request):
    return render(request, "UserHome.html")


def login(request):
    msg = ""
    try:
        if request.POST:
            uname = request.POST["t1"]
            password = request.POST["t2"]
            data = Login.objects.filter(Q(uname=uname) & Q(password=password))
            print("data=", data[0].role)
            request.session["uname"] = uname
            print("####################################################")
            if (data[0].role == "admin"):
                return HttpResponseRedirect("/Adminviewfarmer")
            elif (data[0].role == "Farmer"):
                return HttpResponseRedirect("/UserHome")
            elif (data[0].role == "Delivary"):
                return HttpResponseRedirect("/delivaryviewcrop")
            else:
                msg = "Invalid Username or password"
    except:
        msg = "Invalid Username or password"

    return render(request, "login.html", {"msg": msg})


def registration(request):
    msg = ""
    if request.POST:
        name = request.POST["t1"]
        gender = request.POST["t2"]
        email = request.POST["t3"]
        phone = request.POST["t4"]
        password = request.POST["t5"]
        if Registration.objects.filter(email=email, phone=phone).exists() or Login.objects.filter(uname=email).exists():
            msg = "Email Already Registered"
        else:
            obj1 = Login.objects.create(
                uname=email, password=password, role='Farmer')
            obj1.save()
            obj = Registration.objects.create(
                name=name, gender=gender, email=email, phone=phone, logid=obj1)
            obj.save()
            msg = "Registration successfully"
        # else:
        #     msg="Username already exist"
    return render(request, "Addfarmer.html", {"msg": msg})


def addfarmer(request):
    msg = ""
    if request.POST:
        name = request.POST["t1"]
        gender = request.POST["t2"]
        email = request.POST["t3"]
        phone = request.POST["t4"]
        password = request.POST["t5"]
        if Registration.objects.filter(email=email, phone=phone).exists() or Login.objects.filter(uname=email).exists():
            msg = "Email Already Registered"
        else:
            obj1 = Login.objects.create(
                uname=email, password=password, role='Farmer')
            obj1.save()
            obj = Registration.objects.create(
                name=name, gender=gender, email=email, phone=phone, logid=obj1)
            obj.save()
            msg = "Registration successfully"
    return render(request, "Addfarmer.html", {"msg": msg})


def updatefarmer(request):
    msg = ""
    id = request.GET.get("id")
    uname = request.session["uname"]
    print(uname)
    abc = Registration.objects.filter(id=id)
    uemail = abc[0].email
    if request.POST:
        name = request.POST["t1"]
        gender = request.POST["t2"]
        email = request.POST["t3"]
        phone = request.POST["t4"]
        password = request.POST["t5"]
        updatedata = Registration.objects.filter(id=id).update(
            name=name, email=email, phone=phone, gender=gender)
        print(updatedata)
        logdata = Login.objects.filter(uname=uemail).update(
            uname=email, password=password)
        print(logdata)
        msg = "updated Successfully"
        return HttpResponseRedirect("/Adminviewfarmer?msg="+msg)
    return render(request, 'updatefarmer.html', {"msg": msg, "abc": abc})


def updatecrop(request):
    msg = ""
    id = request.GET.get("id")
    uname = request.session["uname"]
    print(uname)
    abc = Addcropdetails.objects.filter(id=id)
    if request.POST:
        name = request.POST["t1"]
        qty = request.POST["t3"]
        status = request.POST["t4"]
        date = request.POST["t5"]
        updatedata = Addcropdetails.objects.filter(id=id).update(
            name=name, qty=qty, status=status, date=date)
        print(updatedata)
        msg = "updated Successfully"
        return HttpResponseRedirect("/Adminviewcrop?msg="+msg)
    return render(request, 'updatecrop.html', {"msg": msg, "abc": abc})


def addcrop(request):
    msg = ""
    uname = request.session["uname"]
    if request.POST:
        name = request.POST["t1"]
        qty = request.POST["t3"]
        status = request.POST["t4"]
        date = request.POST["t5"]

        # c.execute("select count(*) from login where uname='"+str(email)+"'")
        # data=c.fetchall()

        obj = Addcropdetails.objects.create(
            name=name, qty=qty, status=status, date=date)
        obj.save()
    return render(request, "Addcrop.html", {"msg": msg})


def deletecrop(request):
    msg = request.GET.get("msg")
    id = request.GET.get("ab")
    did = request.GET.get("did")
    efg = Addcropdetails.objects.filter(id=id).delete()
    msg = "Cancelled"
    return HttpResponseRedirect("/Adminviewcrop", {"msg": msg})


def farmerprofile(request):
    msg = ""
    uname = request.session["uname"]
    data = Registration.objects.filter(Q(email=uname))
    if request.POST:
        name = request.POST["t1"]
        gender = request.POST["t2"]
        email = request.POST["t3"]
        phone = request.POST["t4"]
        password = request.POST["t5"]
        data = Login.objects.get(uname=uname)
        # c.execute("select count(*) from login where uname='"+str(email)+"'")
        # data=c.fetchall()
        if (data):
            obj = Registration.objects.get(email=uname)
            obj.name = name
            obj.phone = phone
            obj.save()
            obj1 = Login.objects.get(email=uname)
            obj1.password = password
            obj1.save()
            msg = "Registration successfully"
        else:
            msg = "Username already exist"
    return render(request, "Farmerprofile.html", {"msg": msg, "data": data})


def Addcropdetails1(request):
    msg = ""
    uname = request.session["uname"]
    data1 = Registration.objects.get(email=uname)

    if request.POST:
        name = request.POST["t1"]

        qty = request.POST["t3"]
        status = request.POST["t4"]
        date = request.POST["t5"]

        # c.execute("select count(*) from login where uname='"+str(email)+"'")
        # data=c.fetchall()

        obj = Addcropdetails.objects.create(
            fid=data1, name=name, qty=qty, status=status, date=date)
        obj.save()
    return render(request, "Farmeraddcrop.html", {"msg": msg})


def farmerviewcrop(request):
    uname = request.session["uname"]
    data1 = Registration.objects.filter(email=uname)
    cmpid = data1[0].id
    data = Addcropdetails.objects.filter(fid=cmpid)
    return render(request, "farmerviewcrop.html", {"data": data})


def Adminviewcrop(request):
    data = Addcropdetails.objects.filter()
    return render(request, "Adminviewcrop.html", {"data": data})


def Adminviewfarmer(request):
    msg = request.GET.get("msg")
    data = Registration.objects.filter()
    return render(request, "Adminviewfarmer.html", {"data": data, "msg": msg})


def deletefarmer(request):
    msg = request.GET.get("msg")
    id = request.GET.get("ab")
    did = request.GET.get("did")
    efg = Registration.objects.filter(id=id).delete()
    abc = Login.objects.filter(id=did).delete()
    msg = "Cancelled"
    return HttpResponseRedirect("/Adminviewfarmer", {"msg": msg})


def AdminaddNews(request):
    abc = Addnews.objects.all()
    if request.POST:
        data = Addnews.objects.create(
            title=request.POST["t3"], news=request.POST["t1"], date=request.POST["t2"])
        data.save()
    return render(request, "AdminaddNews.html", {"abc": abc})


def deletenews(request):
    msg = request.GET.get("msg")
    id = request.GET.get("id")
    efg = Addnews.objects.filter(id=id).delete()
    msg = "Cancelled"
    return HttpResponseRedirect("/AdminaddNews")


def updatenews(request):
    msg = ""
    id = request.GET.get("id")
    uname = request.session["uname"]
    print(uname)
    abc = Addnews.objects.filter(id=id)
    if request.POST:
        updatedata = Addnews.objects.filter(id=id).update(
            title=request.POST["t3"], news=request.POST["t1"], date=request.POST["t2"])
        print(updatedata)
        msg = "updated Successfully"
        return HttpResponseRedirect("/AdminaddNews?msg="+msg)
    return render(request, 'updatenews.html', {"msg": msg, "abc": abc})


def Farmerviewnews(request):
    data = Addnews.objects.filter()
    return render(request, "Farmerviewnews.html", {"data": data})


def Adminaddloantype(request):
    if request.POST:
        obj = Loantype.objects.create(
            type=request.POST["t1"], duration=request.POST["t2"], description=request.POST["t3"], amount=request.POST["t4"])
        obj.save()
    data = Loantype.objects.filter()
    return render(request, "Adminaddloantype.html", {"data": data})


def updateloan(request):
    msg = ""
    id = request.GET.get("id")
    uname = request.session["uname"]
    print(uname)
    abc = Loantype.objects.filter(id=id)
    if request.POST:
        updatedata = Loantype.objects.filter(id=id).update(
            type=request.POST["t1"], duration=request.POST["t2"], description=request.POST["t3"], amount=request.POST["t4"])
        print(updatedata)
        msg = "updated Successfully"
        return HttpResponseRedirect("/Adminaddloantype?msg="+msg)
    return render(request, 'updateloan.html', {"msg": msg, "abc": abc})


def deleteloan(request):
    msg = request.GET.get("msg")
    id = request.GET.get("id")
    efg = Loantype.objects.filter(id=id).delete()
    msg = "Cancelled"
    return HttpResponseRedirect("/Adminaddloantype")


def farmerviewloan(request):
    data = Loantype.objects.filter()
    return render(request, "farmerviewloan.html", {"data": data})


def farmerrequestloan(request):
    id = request.GET["id"]
    data = Loantype.objects.filter(Q(id=id))
    if request.POST:
        obj1 = Registration.objects.get(email=request.session["uname"])
        obj2 = Loantype.objects.get(id=id)
        obj3 = Loanrequest.objects.create(
            loanid=obj2, uid=obj1, requestamount=request.POST["t3"], status='Requested', date=request.POST["t4"])
        obj3.save()
    return render(request, "Farmerrequestloan.html", {"data": data})


def farmerviewloanstatus(request):
    obj1 = Registration.objects.get(email=request.session["uname"])
    data = Loanrequest.objects.filter(Q(uid=obj1))
    return render(request, "Farmerviewloanstatus.html", {"data": data})


def collectcrop(request):
    id = request.GET["id"]
    data = Loantype.objects.filter(Q(id=id))
    if request.POST:
        obj1 = delivaryboy.objects.get(email=request.session["uname"])
        obj2 = Addcropdetails.objects.get(id=id)
        request.session["pay"] = request.POST["t3"]
        obj3 = delivary.objects.create(
            did=obj1, cropid=obj2, amount=request.POST["t3"], date=request.POST["t4"])
        obj3.save()
        return HttpResponseRedirect("/payment1")
    return render(request, "collectcrop.html", {"data": data})


def delivaryviewcrop(request):
    data = Addcropdetails.objects.filter()
    return render(request, "delivaryviewcrop.html", {"data": data})


def adminviewcropcollection(request):
    data = delivary.objects.filter()
    return render(request, "adminviewcropcollection.html", {"data": data})

def adminadddelivaryboy(request):
    msg = ""
    msg = request.GET.get("msg")
    abc = delivaryboy.objects.all()
    if request.POST:
        if request.POST:
            name = request.POST["t1"]
            gender = request.POST["t2"]
            email = request.POST["t3"]
            phone = request.POST["t4"]
            password = request.POST["t5"]
            if delivaryboy.objects.filter(email=email, phone=phone).exists() or Login.objects.filter(uname=email).exists():
                msg = "Email Already Registered"
            else:
                obj1 = Login.objects.create(
                    uname=email, password=password, role='Delivary')
                obj1.save()
                obj = delivaryboy.objects.create(
                    name=name, gender=gender, email=email, phone=phone, logid=obj1)
                obj.save()
                msg = "Registration successfully"
    return render(request, "adminadddelivaryboy.html", {"msg": msg, "abc": abc})

def deletedeliveryboy(request):
    msg = request.GET.get("msg")
    id = request.GET.get("ab")
    did = request.GET.get("did")
    efg = delivaryboy.objects.filter(id=id).delete()
    abc = Login.objects.filter(id=did).delete()
    msg = "Cancelled"
    return HttpResponseRedirect("/Adminviewfarmer", {"msg": msg})

def updatedeliveryboy(request):
    msg = ""
    id = request.GET.get("id")
    uname = request.session["uname"]
    print(uname)
    abc = delivaryboy.objects.filter(id=id)
    uemail = abc[0].email
    if request.POST:
        name = request.POST["t1"]
        gender = request.POST["t2"]
        email = request.POST["t3"]
        phone = request.POST["t4"]
        password = request.POST["t5"]
        updatedata = delivaryboy.objects.filter(id=id).update(
            name=name, email=email, phone=phone, gender=gender)
        print(updatedata)
        logdata = Login.objects.filter(uname=uemail).update(
            uname=email, password=password)
        print(logdata)
        msg = "updated Successfully"
        return HttpResponseRedirect("/adminadddelivaryboy?msg="+msg)
    return render(request, 'updatedelivaryboy.html', {"msg": msg, "abc": abc})


def payment1(request):
    msg = ""
    count = 0
    uname = request.session["uname"]

    if request.POST:
        card = request.POST.get("test")
        request.session["card"] = card
        cardno = request.POST.get("cardno")
        request.session["card_no"] = cardno
        pinno = request.POST.get("pinno")
        request.session["pinno"] = pinno
        return HttpResponseRedirect("/payment2")

    return render(request, "payment1.html", {"msg": msg, "uname": uname})


def payment2(request):
    cno = request.session["card_no"]
    amount = request.session["pay"]
    if request.POST:
        # name=request.POST.get("t1")
        # request.session["m"]=name
        # address=request.POST.get("t2")
        # email=request.POST.get("t3")
        # phno=request.POST.get("t4")
        # n="insert into delivery values('"+str(cno)+"','"+str(name)+"','"+str(address)+"','"+str(email)+"','"+str(phno)+"','"+str(amount)+"')"
        # print(n)
        # c.execute(n)
        # con.commit()
        return HttpResponseRedirect("/payment3")
    return render(request, "payment2.html", {"cno": cno, "amount": amount})


def payment3(request):
    return render(request, "payment3.html")


def payment4(request):
    return render(request, "payment4.html")


def payment5(request):
    cno = request.session["card_no"]
    today = "05/05/2000"
    # name =  request.session['name']
    amount = request.session["pay"]
    return render(request, "payment5.html", {"cno": cno, "today": today, "amount": amount})


def adminviewloan(request):

    data = Loanrequest.objects.filter()
    return render(request, "Adminviewloan.html", {"data": data})
