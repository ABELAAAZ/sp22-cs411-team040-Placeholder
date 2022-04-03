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
                    if username == 'admin':
                        return redirect('/adminpage/')
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
        cursor.execute("select c_name,rarity, img,type,status,cardID from Card natural join OwnedCard where userID =%s",
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
    returnlist = []
    for i in range(5):
        m = random.randint(1, 1000)
        if box_infor[0] == 'Fire' or box_infor[0] == 'Water' or box_infor[0] == 'Grass':
            if m <= box_pro[0] * 1000:
                cursor.execute(
                    "select cardNo,img ,c_name from Card where type = %s and rarity = %s order by Rand() limit 1",
                    [box_infor[0], 'A'])
                card_infor = cursor.fetchone()
                cardNo = card_infor[0]

                cursor.execute("Insert into OwnedCard (cardNo,userID,status,c_price) values(%s,%s,%s,%s)",
                               [cardNo, userid, 'owned', 0.0])
                returnlist.append([card_infor[2], 'A', card_infor[1]])

            elif m <= (box_pro[0] + box_pro[1]) * 1000:
                cursor.execute(
                    "selectcardNo,img ,c_name from Card where type = %s and rarity = %s order by Rand() limit 1",
                    [box_infor[0], 'B'])
                card_infor = cursor.fetchone()
                cardNo = card_infor[0]
                cursor.execute("Insert into OwnedCard (cardNo,userID,status,c_price) values(%s,%s,%s,%s)",
                               [cardNo, userid, 'owned', 0.0])
                returnlist.append([card_infor[2], 'B', card_infor[1]])
            elif m <= (box_pro[0] + box_pro[1] + box_pro[2]) * 1000:
                cursor.execute(
                    "select cardNo,img ,c_name from Card where type = %s and rarity = %s order by Rand() limit 1",
                    [box_infor[0], 'C'])
                card_infor = cursor.fetchone()
                cardNo = card_infor[0]
                cursor.execute("Insert into OwnedCard (cardNo,userID,status,c_price) values(%s,%s,%s,%s)",
                               [cardNo, userid, 'owned', 0.0])
                returnlist.append([card_infor[2], 'C', card_infor[1]])
            else:
                cursor.execute(
                    "select cardNo,img ,c_name from Card where type = %s and rarity = %s order by Rand() limit 1",
                    [box_infor[0], 'D'])
                card_infor = cursor.fetchone()
                cardNo = card_infor[0]
                cursor.execute("Insert into OwnedCard (cardNo,userID,status,c_price) values(%s,%s,%s,%s)",
                               [cardNo, userid, 'owned', 0.0])
                returnlist.append([card_infor[2], 'D', card_infor[1]])
        else:
            if m <= box_pro[0] * 1000:
                cursor.execute("select cardNo,img ,c_name from Card where rarity = %s order by Rand() limit 1",
                               ['A'])
                card_infor = cursor.fetchone()
                cardNo = card_infor[0]
                cursor.execute("Insert into OwnedCard (cardNo,userID,status,c_price) values(%s,%s,%s,%s)",
                               [cardNo, userid, 'owned', 0.0])
                returnlist.append([card_infor[2], 'A', card_infor[1]])

            elif m <= (box_pro[0] + box_pro[1]) * 1000:
                cursor.execute("select cardNo,img ,c_name from Card where rarity = %s order by Rand() limit 1",
                               ['B'])
                card_infor = cursor.fetchone()
                cardNo = card_infor[0]
                cursor.execute("Insert into OwnedCard (cardNo,userID,status,c_price) values(%s,%s,%s,%s)",
                               [cardNo, userid, 'owned', 0.0])
                returnlist.append([card_infor[2], 'B', card_infor[1]])
            elif m <= (box_pro[0] + box_pro[1] + box_pro[2]) * 1000:
                cursor.execute("select cardNo,img ,c_name from Card where rarity = %s order by Rand() limit 1",
                               ['C'])
                card_infor = cursor.fetchone()
                cardNo = card_infor[0]
                cursor.execute("Insert into OwnedCard (cardNo,userID,status,c_price) values(%s,%s,%s,%s)",
                               [cardNo, userid, 'owned', 0.0])
                returnlist.append([card_infor[2], 'C', card_infor[1]])
            else:
                cursor.execute("select cardNo,img ,c_name from Card where rarity = %s order by Rand() limit 1",
                               ['D'])
                card_infor = cursor.fetchone()
                cardNo = card_infor[0]
                cursor.execute("Insert into OwnedCard (cardNo,userID,status,c_price) values(%s,%s,%s,%s)",
                               [cardNo, userid, 'owned', 0.0])
                returnlist.append([card_infor[2], 'D', card_infor[1]])

    cursor.execute(
        "Insert into BoxOrder (userID,boxID,pay_datetime,pay_amount) values(%s,%s,%s,%s);",
        [userid, int(boxid), paydate, price])
    """returnlist = [['Manaphy','D',
                   'https://content.tcgcollector.com/content/images/b6/bc/e2/b6bce232b85a26fd67ef2be7e0d07a40790ebe5ccb047ab41a8d6102689211f3.jpg'],
                  ['Noivern','D',
                   'https://content.tcgcollector.com/content/images/b8/d1/3b/b8d13bc33436898e384b505fbade923c7604701fac5335900d876ad7cdb78090.jpg']]"""
    return HttpResponse(json.dumps(returnlist))


def modifycard(request):
    price = request.POST.get('price')
    status = request.POST.get('status')
    cardID = request.POST.get('cardID')
    cursor = connection.cursor()
    if status == 'selling':
        cursor.execute("update OwnedCard set status = %s, c_price = %s where cardID = %s", ['selling', price, cardID])
    else:
        cursor.execute("update OwnedCard set status = %s, c_price = %s where cardID = %s", ['owned', 0, cardID])

    return redirect('/mypokemon/')


def resalepage(request):
    if request.session.get('is_login', None):
        cursor = connection.cursor()
        cursor.execute("select * from OwnedCard natural join Card where status='selling'")
        resalecard = cursor.fetchall()
        return render(request, 'resalepage.html', {'resalecardlist': resalecard})
    else:
        return redirect('/login/')


def buyonecard(request):
    cardID = request.POST.get('cardID')
    buyer = request.session.get('userID', None)
    today = datetime.date.today()
    paydate = today.strftime('%y%m%d')

    cursor = connection.cursor()
    cursor.execute("select * from OwnedCard where cardID =%s", cardID)
    card = cursor.fetchone()
    cursor.execute(
        "Insert into ResaleOrder (sellerID,buyerID,cardID,trade_amount,trade_datetime) values(%s,%s,%s,%s,%s)",
        [card[2], buyer, cardID, card[4], paydate])
    cursor.execute("update OwnedCard set status = %s, c_price = %s, userID = %s where cardID = %s",
                   ['owned', 0, buyer, cardID])
    return HttpResponse(json.dumps(cardID))


def resalehistory(request):
    if request.session.get('is_login', None):
        cursor = connection.cursor()
        userID = request.session.get('userID', None)
        cursor.execute(
            "select r_orderID, c_name, rarity, b.u_name, y.u_name, trade_amount, trade_datetime from (select r_orderID, c_name, rarity, u_name, buyerID, trade_amount, trade_datetime from (select r_orderID, c_name, rarity, sellerID, buyerID, trade_amount, trade_datetime from ResaleOrder natural join OwnedCard natural join Card where buyerID = %s or sellerID = %s) a left join User x on a.sellerID = x.userID) b left join User y on b.buyerID = y.userID",
            [userID, userID]
        )
        resalehistorylist = cursor.fetchall()
        return render(request, 'resalehistory.html', {'resalehistorylist': resalehistorylist})
    else:
        return redirect('/login/')



def showpricetrend(request):
    # TODO
    trendlist = [[20220202, 10], [20220218, 9], [20220401, 15]]
    return HttpResponse(json.dumps(trendlist))

def deleteboxhistory(request):
    orderID = request.POST.get('orderID')
    cursor = connection.cursor()
    cursor.execute(
        " delete from BoxOrder where b_orderID  = %s",orderID)
    return redirect('/boxhistory/')


def searchbox(request):
    if request.method == "POST":
        keyword = request.POST.get('keyword', None)
        cursor = connection.cursor()
        keyword = "%" + str(keyword) + "%"
        print(keyword)
        cursor.execute("select * from BlindBox where title like %s", keyword)
        searchedcard = cursor.fetchall()
        print(searchedcard)
    return render(request, 'mainpage.html', {'blindboxlist': searchedcard})


def pricecheck(request):
    if request.session.get('is_login', None):

        return render(request, 'pricecheck.html')
    else:
        return redirect('/login/')


def adminpage(request):
    # todo 显示一个default的table表
    return render(request, 'adminpage.html')


def adminsearch(request):
    return 1