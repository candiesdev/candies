from django.urls import path
from . import views

app_name = 'usr'
urlpatterns = [
    path('', views.sessionView, name='sessionview'),
    path("<str:action>/", views.sessionView, name="session"),
    path("<str:action>/<str:reverseSite>/", views.sessionView, name="session"),
]