from django.shortcuts import render
from .models import A
from django.http import HttpResponse

def home(request):
    return render(request, 'main/main.html')

def cpu(request):
    c = {
        'asd':A.objects.all()
    }
    print(c.get('asd'))
    return render(request, 'main/cpu.html', c)