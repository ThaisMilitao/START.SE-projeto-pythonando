from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.messages import constants

# Create your views here.
def register(request):
    if request.method == "GET":
        return render(request,'register.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('senha')
        donfirm_password = request.POST.get('confirmar_senha')
        if not password == donfirm_password:
            messages.add_message(request, constants.ERROR, 'As senhas devem ser iguais')
            return redirect('/users/register')

        if len(password) < 6:
            messages.add_message(request, constants.ERROR, 'A senha deve possuir pelo menos 6 caracteres')
            return redirect('/users/register')

        users = User.objects.filter(username=username)
        if users.exists():
            messages.add_message(request, constants.ERROR, 'User exists')
            return redirect('/users/register')
        user = User.objects.create_user(
        username=username,
        password=password)
    return redirect('/users/login')

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('senha')
        user = auth.authenticate(request, username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('/businessman/register_company')
    messages.add_message(request, constants.ERROR, 'Usuario ou senha inválidos')
    return redirect('/users/login')
