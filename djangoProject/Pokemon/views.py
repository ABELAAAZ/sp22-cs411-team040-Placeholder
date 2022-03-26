# Create your views here.
from django.shortcuts import render
from django.db import connection


def login(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        message = "所有字段都必须填写！"

        if username and password:
            username = username.strip()
            #try:
            cursor = connection.cursor()
            cursor.execute("select password from User where u_name=%s " ,username)
            result = cursor.fetchone();
            if result[0]==password:
                message='password match'
            else:
                message = "password not correct！"
            #except:
            #    message = "username doesn't exist！"
        return render(request, 'login.html', {"message": message})
    else:
        return render(request, 'login.html')



def mainpage(request):

    return render(request, 'mainpage.html')