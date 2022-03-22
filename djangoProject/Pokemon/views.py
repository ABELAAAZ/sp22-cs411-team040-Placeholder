# Create your views here.
from django.shortcuts import render



def login(request):
    context = {}
    context['welcome'] = 'yyy'
    return render(request, 'login.html', context)