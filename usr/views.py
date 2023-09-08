from ast import Pass
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.db.models import Case, When, Value, IntegerField, Q
from django.utils import timezone
from django.core.mail import send_mail
from django.urls import reverse
from .models import MenuItem

from .forms import SessionLogin, SessionAuthenticate

# Session Views

def menuConstructor(itemsList):
    item="title"
    q = Q()
    for itemValue in itemsList:
        q |= Q(**{item: itemValue})
    ordering = Case(
        When(q & Q(title='Retornar'), then=Value(0)),
        When(q & Q(title='Autenticar'), then=Value(1)),
        When(q & Q(title='Inicio'), then=Value(2)),
        default=Value(3),
        output_field=IntegerField(),
        )
    menuItems = MenuItem.objects.filter(q).order_by(ordering)
    return menuItems

def sessionView(request):
    action = alert = ""
    prev = "/usr"
    userId = ""
    userEmail = ""
    sessionTemplate = ""
    loginData = {}
    activeApp = "login"

    if request.method == "POST":
        if "action" in request.POST:
            action = request.POST["action"]
        if "prev" in request.POST:
            prev = request.POST["prev"]
    elif "action" in request.GET:
        action = request.GET["action"]
    if "prev" in request.GET:
        prev = request.GET["prev"]

    if request.user.is_authenticated:
        logged = True
        alert = "Autenticado"
    else:
        alert = "No autenticado"
        logged = False

    if logged and (action == "login" or action == "password" or action == "authenticate"):
        return redirect(prev)
    elif action == "login":
        logged = False
        alert = "No autenticado"
        action = "enterPass"
        sessionTemplate = "userLogin"
        sessionForm = SessionLogin()
        loginData.update({
        "action": action,
        "prev": prev,
        "alert": alert,
        "sessionTemplate" : sessionTemplate,
        "sessionForm" : sessionForm,
        "activeApp": activeApp})
        return render(request, "usr/sessionindex.html", loginData)
    elif action == "enterPass":
        userId = request.POST["userId"]
        logged = False
        alert = "No autenticado"
        if User.objects.filter(username=request.POST["userId"]).exists():
            action = "authenticate"
            sessionTemplate = "userPass"
            sessionForm = SessionAuthenticate(userId)
            loginData.update({
            "action": action,
            "prev": prev,
            "alert": alert,
            "sessionTemplate" : sessionTemplate,
            "sessionForm" : sessionForm,
            "activeApp": activeApp})
            return render(request, "usr/sessionindex.html", loginData)
        else:
            alert = "user_error"
            action = "login"
            sessionTemplate = "userError"
            loginData.update({
            "action": action,
            "prev": prev,
            "alert": alert,
            "sessionTemplate" : sessionTemplate,
            "userId": userId,
            "activeApp": activeApp})
            return render(request, "usr/sessionindex.html", loginData)
    elif action == "authenticate":
        if request.method == 'POST':
            username = request.POST['userId']
            password = request.POST['userPass']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                loggedIn = True
                return redirect(prev)
            else:
                alert = "password_error"
                action = "login"
                sessionTemplate = "passwordError"
                loginData.update({
                "action": action,
                "prev": prev,
                "alert": alert,
                "sessionTemplate" : sessionTemplate,
                "userId": userId,
                "activeApp": activeApp})
                return render(request, "usr/sessionindex.html", loginData)

    elif logged and action == "logout":
        logout(request)
        alert = "No autenticado"
        logged = False
        return redirect(prev)
    elif action == "logout":
        try:
            logout(request)
            logged = False
            return redirect(prev)
        except:
            return redirect(prev)
    elif logged:
        itemsList = ["Salir", "Inicio"]
        if prev!="/usr":
            itemsList.append("Retornar")
        menuItems = menuConstructor(itemsList)

        sessionMenu = {}
        for menu in menuItems:
            title = menu.title
            titleUrl = menu.url
            if title == "Retornar":
                titleUrl = prev
            sessionMenu.update({ title : titleUrl })

        logged = True
        alert = "Autenticado"
        sessionTemplate = "userInfo"
        userId = request.user.username
        userEmail = request.user.email
        loginData.update({
        "action": action,
        "prev": prev,
        "alert": alert,
        "sessionTemplate" : sessionTemplate,
        "userId": userId,
        "userEmail": userEmail,
        "sessionMenu" : sessionMenu,
        "activeApp": activeApp})
        return render(request, "usr/sessionindex.html", loginData)
    else:
        itemsList = ["Autenticar", "Inicio"]
        if prev!="/usr":
            itemsList.append("Retornar")
        menuItems = menuConstructor(itemsList)

        sessionMenu = {}
        for menu in menuItems:
            title = menu.title
            titleUrl = menu.url
            if title == "Retornar":
                titleUrl = prev
            sessionMenu.update({ title : titleUrl })

        sessionTemplate = "sessionIndex"
        loginData.update({
        "sessionTemplate" : sessionTemplate,
        "sessionMenu" : sessionMenu,
        "activeApp": activeApp})
        return render(request, "usr/sessionindex.html", loginData)