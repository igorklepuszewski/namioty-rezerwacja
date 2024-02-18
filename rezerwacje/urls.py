"""
URL configuration for namioty project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# importy widokow
from rezerwacje.views import NamiotListView, reserve, NamiotDetailView, unreserve, RezerwacjaListView

urlpatterns = [
    path('', NamiotListView.as_view(), name="index"),
    path('rezerwacje', RezerwacjaListView.as_view(), name="rezerwacje"),
    path('reserve/<int:namiot_id>', reserve, name="reserve"),
    path('unreserve/<int:rezerwacja_id>', unreserve, name="unreserve"),
    path('<int:pk>', NamiotDetailView.as_view(), name="details")
]