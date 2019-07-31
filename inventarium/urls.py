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
    path('register/terms/', views.terms, name='terms'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('profile/', views.profile, name='profile'),
    path('profile/update', views.profile_update, name='profile_update'),
    path('profile/delete', views.user_delete, name='user_delete'),
    path('about/', views.about, name='about'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/residence_add', views.residence_add, name='residence_add'),
    path('residence/<int:residence_id>', views.residence, name='residence'),
    path('residence/<int:residence_id>/update',
         views.residence_update, name='residence_update'),
    path('residence/<int:residence_id>/delete', views.residence_delete,
         name='residence_delete'),

    path('room/<int:room_id>/', views.room, name='room'),
    path('room/<int:room_id>/list', views.room_list, name='room_list'),
    path('room/<int:room_id>/<record>/', views.room_equipment,
         name='room_equipment'),
    path('room/<int:residence_id>/add', views.room_add, name='room_add'),
    path('room/<int:room_id>/update', views.room_update, name='room_update'),
    path('room/<int:room_id>/delete', views.room_delete, name='room_delete'),

    path('equipment/<int:equipment_id>/', views.equipment, name='equipment'),
    path('equipment/<int:room_id>/add/', views.equipment_add,
         name='equipment_add'),
    path('equipment/<int:equipment_id>/update',
         views.equipment_update, name='equipment_update'),
    path('equipment/<int:equipment_id>/delete/',
         views.equipment_delete, name='equipment_delete'),

    path('search/', views.search, name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
