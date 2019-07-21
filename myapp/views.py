from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from myapp.models import Problem


def index(request):
    user = User.objects.get(pk=1)
    group = user.groups.all()
    if request.user.is_authenticated:
        if group == 'Fixer':
            return render(request, 'fixer.html')
        else:
            problems = Problem.objects.all()
            return render(request, "index.html", {'problems': problems})
    else:
        return redirect('/login')

def openmyproblems(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            problems_u = Problem.objects.filter(status='Не выполнено', author=request.user)
            return render(request, 'my_problem.html', {'problems_u': problems_u})

def openmysolvedproblems(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            prblems_i = Problem.objects.filter(status='Выполнено', author=request.user)
            return render(request, 'mysolvedproblems.html', {'prblems_i': prblems_i})

def CreateProblem(request):
    if request.method == 'GET':
        return render(request, 'Create.html')
    if request.method == 'POST':
        problem = Problem()
        problem.text = request.POST['Problem']
        problem.room = request.POST['Number']
        problem.author = request.user
        problem.save()
        return redirect('/')

def login_page(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('login', '')
        password = request.POST.get('password', '')

        if username == '' or password == '':
            messages.error(request, 'Заполните все поля!')
            return redirect('/login')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Неправильный логин или пароль!')
            return redirect('/login')


def register(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'register.html')
    if request.method == 'POST':
        username = request.POST.get('login', '')
        password = request.POST.get('password', '')
        email = request.POST.get('email', '')

        if username == '' or password == '' or email == '':
            messages.error(request, 'Заполните все поля')
            return redirect('/register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Логин занят")
            return redirect('/register')

        # создаем пользователя
        user = User.objects.create_user(username, email, password)
        user.save()

        # "входим" пользователя
        login(request, user)

        return redirect('/')

def logout_page(request):
    if request.method == 'POST':
        logout(request)
    return redirect('/login')