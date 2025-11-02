from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

# Главная страница портала
def index(request):
    # Простая главная страница с информацией о студии
    return render(request, 'design_app/index.html', {'title': 'Design.pro — Студия Дизайна'})

# Страница регистрации нового пользователя
def register_user(request):
    if request.user.is_authenticated:
        return redirect('index') # Если пользователь уже вошел, перенаправляем на главную

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Можно сразу авторизовать пользователя после регистрации
            login(request, user)
            messages.success(request, f"Успешная регистрация! Добро пожаловать, {user.username}!")

            return redirect('index')
        else:
            messages.error(request, "Ошибка регистрации. Пожалуйста, проверьте введенные данные.")
    else:
        form = UserCreationForm()

    context = {
        'form': form,
        'title': 'Регистрация'
    }
    return render(request, 'design_app/register.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('index') # Если пользователь уже вошел, перенаправляем на главную

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"С возвращением, {username}!")

                return redirect('index')
            else:
                messages.error(request, "Неверный логин или пароль.")
        else:
            messages.error(request, "Неверный логин или пароль.")
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
        'title': 'Вход в Личный Кабинет'
    }
    return render(request, 'design_app/login.html', context)

# Функция выхода
def logout_user(request):
    logout(request)
    messages.info(request, "Вы вышли из системы.")
    return redirect('index')
