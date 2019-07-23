"""inventarium URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('profile/', views.profile, name='profile'),
    path('profile/update', views.profile_update, name='profile_update'),
    path('about/', views.about, name='about'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/residence_add', views.residence_add, name='residence_add'),
    path('residence/<residence_id>', views.residence, name='residence'),
    path('residence/<residence_id>/update',
         views.residence_update, name='residence_update'),

    path('room/<room_id>/', views.room, name='room'),
    path('room/<residence_id>/add', views.room_add, name='room_add'),
    path('room/<room_id>/update', views.room_update, name='room_update'),
    # TODO [23 Juillet 2019]: add room_update template

    path('equipment/<equipment_id>/', views.equipment, name='equipment'),
    path('equipment/add/<room_id>/', views.equipment_add, name='equipment_add'),
    path('equipment/update/<equipment_id>/',
         views.equipment_update, name='equipment_update'),
    # TODO [23 Juillet 2019]: add equipment_update template
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
