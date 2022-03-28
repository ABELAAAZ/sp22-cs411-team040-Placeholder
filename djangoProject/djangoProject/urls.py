"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Pokemon import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import staticfiles

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('mainpage/', views.mainpage),
    path('logout/', views.logout),
    path('signup/', views.signup),
    path('mypokemon/', views.mypokemon),
    path('boxhistory/', views.boxhistory),
    path('buyonebox/', views.buyonebox),
  #  path('/buybox/boxid/', views.buybox, name='buybox'),

]

urlpatterns += staticfiles_urlpatterns()
