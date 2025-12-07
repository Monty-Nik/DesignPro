from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Путь 'superadmin' ведет в стандартную админ-панель Django
    path('superadmin/', admin.site.urls),

    # Все остальные URL (главная, логин, профиль и т.д.)
    # обрабатываются в приложении design_app
    path('', include('design_app.urls')),
]

# Это необходимо для обслуживания медиа-файлов (загруженных планов)
# в режиме разработки (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
