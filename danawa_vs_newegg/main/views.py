from django.shortcuts import render

posts = [
    {
        'author': 'aa',
        'title': 'bb'
    },
    {
        'author': 'cc',
        'title': 'dd'
    }
]

def home(request):
    context = {
        'posts':posts
    }
    return render(request, 'main/main.html', context)

def cpu(request):

    return render(request, 'main/cpu.html')