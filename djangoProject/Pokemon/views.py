# Create your views here.
from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse

def login(request):
    if request.session.get('is_login', None):
        return redirect('/mainpage/')

    else:
        if request.method == "POST":
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            message = ""

            if username and password:
                username = username.strip()
                cursor = connection.cursor()
                cursor.execute("select * from User where u_name=%s limit 1", username)
                result = cursor.fetchone()

                if result[1] == password:
                    message = 'password match'
                    request.session['username'] = username
                    request.session['userID'] = result[0]
                    request.session['is_login'] = True
                    return redirect('/mainpage/')
                else:
                    message = "password not correct！"
            else:
                message = "Please enter both username and Password"

            return render(request, 'login.html', {"message": message})
        else:
            return render(request, 'login.html')


def logout(request):
    if request.session.get('is_login', None):
        request.session.flush()
        return redirect("/login/")


def mainpage(request):
    if request.session.get('is_login', None):
        cursor = connection.cursor()
        cursor.execute("select * from BlindBox")
        blindboxlist = cursor.fetchall()
        return render(request, 'mainpage.html', {'blindboxlist': blindboxlist})
    else:
        return redirect('/login/')




def signup(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        passwordconfirm = request.POST.get('passwordconfirm', None)
        message = ""

        if username and password and passwordconfirm:
            if passwordconfirm == password:
                cursor = connection.cursor()
                cursor.execute("Select * from User where u_name= %s", username)
                is_existed = cursor.fetchall()
                if not is_existed:
                    cursor.execute("Insert into User (password,u_name) values(%s,%s)", [password, username])
                    return redirect("/login/")
                else:
                    message = "This username already exists, please change another one"
            else:
                message = "Password doesn't match"
        else:
            message = "you should enter all of the fields"

        return render(request, 'signup.html', {"message": message})
    else:
        return render(request, 'signup.html')


def mypokemon(request):
    if request.session.get('is_login', None):
        cursor = connection.cursor()
        userID = request.session.get('userID', None)
        cursor.execute("select c_name,rarity, img,type,status from Card natural join OwnedCard where userID =%s",
                       userID)
        cardlist = cursor.fetchall()
        return render(request, 'mypokemon.html', {'cardlist': cardlist})
    else:
        return redirect('/login/')


def boxhistory(request):
    if request.session.get('is_login', None):
        cursor = connection.cursor()
        userID = request.session.get('userID', None)
        cursor.execute(
            "select b_orderID, title ,pay_amount,pay_datetime from BoxOrder natural join BlindBox where userID =%s",
            userID)
        boxhistorylist = cursor.fetchall()
        return render(request, 'boxhistory.html', {'boxhistorylist': boxhistorylist})
    else:
        return redirect('/login/')


def buybox(request, boxid):
    print(boxid)

def buyonebox(request):
    boxid = request.POST.get('boxid')

    print(boxid)
    return HttpResponse(boxid)