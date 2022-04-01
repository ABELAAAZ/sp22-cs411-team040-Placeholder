# Create your views here.
import random
import json
from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
import datetime


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


def buyonebox(request):
    boxid = request.POST.get('boxid')
    userid = request.session.get('userID', None)
    today = datetime.date.today()
    paydate = today.strftime('%y%m%d')
    cursor = connection.cursor()
    # print('go')
    cursor.execute("select b_price from BlindBox where boxID =%s", boxid)
    price = cursor.fetchone()
    price = price[0]
    # print(userid,int(boxid),paydate,price)
    cursor.execute("select title, rarity, prob from BlindBox natural join Probability where boxID = %s", boxid)
    box_pro = []
    for i in range(4):
        box_infor = cursor.fetchone()
        box_pro.append(box_infor[2])
    print(box_pro)
    for i in range(5):
        m = random.randint(1, 1000)
        if box_infor[0] == 'Fire' or box_infor[0] == 'Water' or box_infor[0] == 'Grass':
            if m <= box_pro[0] * 1000:
                cursor.execute("select cardNo from Card where type = %s and rarity = %s order by Rand() limit 1",
                               [box_infor[0], 'A'])
                cardNo = cursor.fetchone()
                cardNo = cardNo[0]
                cursor.execute("Insert into OwnedCard (cardNo,userID,status,c_price) values(%s,%s,%s,%s)",
                               [cardNo, userid, 'owned', 0.0])

            elif m <= (box_pro[0] + box_pro[1]) * 1000:
                cursor.execute("select cardNo from Card where type = %s and rarity = %s order by Rand() limit 1",
                               [box_infor[0], 'B'])
                cardNo = cursor.fetchone()
                cardNo = cardNo[0]
                cursor.execute("Insert into OwnedCard (cardNo,userID,status,c_price) values(%s,%s,%s,%s)",
                               [cardNo, userid, 'owned', 0.0])
            elif m <= (box_pro[0] + box_pro[1] + box_pro[2]) * 1000:
                cursor.execute("select cardNo from Card where type = %s and rarity = %s order by Rand() limit 1",
                               [box_infor[0], 'C'])
                cardNo = cursor.fetchone();
                cardNo = cardNo[0]
                cursor.execute("Insert into OwnedCard (cardNo,userID,status,c_price) values(%s,%s,%s,%s)",
                               [cardNo, userid, 'owned', 0.0])
            else:
                cursor.execute("select cardNo from Card where type = %s and rarity = %s order by Rand() limit 1",
                               [box_infor[0], 'D'])
                cardNo = cursor.fetchone()
                cardNo = cardNo[0]
                cursor.execute("Insert into OwnedCard (cardNo,userID,status,c_price) values(%s,%s,%s,%s)",
                               [cardNo, userid, 'owned', 0.0])

    cursor.execute(
        "Insert into BoxOrder (userID,boxID,pay_datetime,pay_amount) values(%s,%s,%s,%s);",
        [userid, int(boxid), paydate, price])
    returnlist = [['Manaphy',
                   'https://content.tcgcollector.com/content/images/b6/bc/e2/b6bce232b85a26fd67ef2be7e0d07a40790ebe5ccb047ab41a8d6102689211f3.jpg'],
                  ['Noivern',
                   'https://content.tcgcollector.com/content/images/b8/d1/3b/b8d13bc33436898e384b505fbade923c7604701fac5335900d876ad7cdb78090.jpg']]
    return HttpResponse(json.dumps(returnlist))


def resalepage(request):
    if request.session.get('is_login', None):
        cursor = connection.cursor()
        cursor.execute("select * from OwnedCard where status='on sale'")
        resalecard = cursor.fetchall()
        return render(request, 'resalepage.html', {'resalecardlist': resalecard})
    else:
        return redirect('/login/')


def resalehistory(request):
    if request.session.get('is_login', None):
        cursor = connection.cursor()
        userID = request.session.get('userID', None)
        cursor.execute(
            # TODO
        )
        boxhistorylist = cursor.fetchall()
        return render(request, 'resalehistory.html', {})
    else:
        return redirect('/login/')
