from django.http import JsonResponse
from django.shortcuts import render, redirect
from core.models import *
#import bcrypt

# Create your views here.
'''
def encrypt(password):
    salt = bcrypt.gensalt(rounds=12)

    password = str.encode(password)

    xpass = bcrypt.hashpw(password, salt)

    new = xpass.decode()

    return new


def passwordCheck(password, saved):
    x = str.encode(saved)

    password = str.encode(password)

    same = bcrypt.checkpw(password, x)

    return same
'''
def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        repass = request.POST.get("repass")
        Type = request.POST.get("type")
        ct = request.POST.get("class")

        try:
            x = Teachers.objects.get(email=email)
            return render(request, "account/signup.html", {"error":"exists"})

        except:
            pass

        if password != repass:
            return render(request, "account/signup.html", {"error":"password-no-match"})

        try:
            lid = Teachers.objects.last().id + 1

        except:
            lid = 1

        if bool(Type) == True:
            #Teachers(id=lid, name=name, email=email, ct=bool(int(Type)), password=encrypt(password), teaches=ct).save()
            Teachers(id=lid, name=name, email=email, ct=bool(int(Type)), password=password, teaches=ct).save()

        else:
            #Teachers(id=lid, name=name, email=email, ct=bool(int(Type)), password=encrypt(password)).save()
            Teachers(id=lid, name=name, email=email, ct=bool(int(Type)), password=password).save()

        request.session["logged-in"] = True
        request.session["email"] = email

        return redirect("/")


    return render(request, "account/signup.html")

def login(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            inst = Teachers.objects.get(email=email)

            #if passwordCheck(password, inst.password):
            if password == inst.password:
                request.session["logged-in"] = True
                request.session["email"] = email

                return redirect("/")


            else:
                return render(request, "account/login.html", {"error":"password"})

        except:
            return render(request, "account/login.html", {"error":"no-exist"})

    return render(request, "account/login.html")


def mobileSignup(request):
    name = request.GET.get("name").strip()
    email = request.GET.get("email").strip()
    password = request.GET.get("password").strip()
    Type = request.GET.get("type").strip()
    ct = request.GET.get("class").strip()

    try:
        x = Teachers.objects.get(email=email)
        return JsonResponse({"message":"Account already exists."})

    except:
        pass

    try:
        x = Teachers.objects.get(name=name)
        return JsonResponse({"message":"Teacher with this name exists. Please enter your full name."})

    except:
        pass

    if bool(Type) == True:
        #Teachers(id=lid, name=name, email=email, ct=bool(int(Type)), password=encrypt(password), teaches=ct).save()
        Teachers(name=name, email=email, ct=bool(Type.capitalize()), password=password, teaches=ct).save()

    else:
        #Teachers(id=lid, name=name, email=email, ct=bool(int(Type)), password=encrypt(password)).save()
        Teachers(name=name, email=email, ct=bool(Type.capitalize()), password=password).save()

    return JsonResponse({"message":True})


def mobileLogin(request):

    email = request.GET.get("email").strip()
    password = request.GET.get("password").strip()

    try:
        inst = Teachers.objects.get(email=email)

        #if passwordCheck(password, inst.password):
        if password == inst.password:

            if inst.ct:
                return JsonResponse({"message":True, "teaches":inst.teaches, "name":inst.name, "email":inst.email})

            else:
                return JsonResponse({"message":True, "name":inst.name, "email":inst.email})


        else:
            return JsonResponse({"message":"Wrong password"})

    except:
        return JsonResponse({"message":"Account does not exist."})


def logout(request):
    del request.session
    return redirect("/account/login")
