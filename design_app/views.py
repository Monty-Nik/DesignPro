from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import RoomPlan
from .forms import CustomUserCreationForm, CustomAuthenticationForm, RoomPlanForm


# Главная страница
def index(request):
    return render(request, 'design_app/index.html', {'title': 'Design.pro — Студия Дизайна'})


# Страница регистрации нового пользователя
def register_user(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Можно сразу авторизовать пользователя после регистрации
            login(request, user)
            messages.success(request, f"Успешная регистрация! Добро пожаловать, {user.username}!")

            return redirect('index')
        else:
            messages.error(request, "Ошибка регистрации. Пожалуйста, проверьте введенные данные.")
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
        'title': 'Регистрация'
    }
    return render(request, 'design_app/register.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')  # Если пользователь уже вошел, перенаправляем на главную

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
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
        form = CustomAuthenticationForm()

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


# личный кабинет пользователя
@login_required
def user_profile(request):
    user_plans = RoomPlan.objects.filter(user=request.user)

    context = {
        'title': 'Личный кабинет',
        'room_plans': user_plans
    }
    return render(request, 'design_app/profile.html', context)


# создание новой заявки
@login_required
def create_room_plan(request):

    if request.method == 'POST':
        form = RoomPlanForm(request.POST, request.FILES)
        if form.is_valid():
            room_plan = form.save(commit=False)
            room_plan.user = request.user
            room_plan.save()
            messages.success(request, 'Заявка успешно создана!')
            return redirect('profile')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = RoomPlanForm()

    context = {
        'title': 'Создание заявки',
        'form': form
    }
    return render(request, 'design_app/create_room_plan.html', context)


# Удаление заявки
@login_required
def delete_room_plan(request, plan_id):
    room_plan = get_object_or_404(RoomPlan, id=plan_id, user=request.user)

    if request.method == 'POST':
        room_plan.delete()
        messages.success(request, 'Заявка успешно удалена!')
        return redirect('profile')

    context = {
        'title': 'Удаление заявки',
        'room_plan': room_plan
    }
    return render(request, 'design_app/delete_room_plan.html', context)