from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application  # Правильный импорт
from .forms import ApplicationForm


@login_required
def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.client = request.user
            application.save()
            messages.success(request, 'Заявка успешно создана!')
            return redirect('my_applications')
    else:
        form = ApplicationForm()
    return render(request, 'applications/create_application.html', {'form': form})


@login_required
def my_applications(request):
    applications = Application.objects.filter(client=request.user)

    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)

    return render(request, 'applications/my_applications.html', {
        'applications': applications
    })