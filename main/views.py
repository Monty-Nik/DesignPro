from django.shortcuts import render
from applications.models import Application


def home(request):
    completed_applications = Application.objects.filter(status='completed')[:4]
    in_progress_count = Application.objects.filter(status='in_progress').count()

    context = {
        'completed_applications': completed_applications,
        'in_progress_count': in_progress_count,
    }
    return render(request, 'main/home.html', context)