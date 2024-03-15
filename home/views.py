from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home/home.html', {})

def apropos(request):
    return render(request, 'home/apropos.html', {})