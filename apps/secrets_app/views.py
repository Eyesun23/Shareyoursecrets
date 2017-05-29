from django.shortcuts import render, redirect, HttpResponse
from .models import User, Secret
from django.contrib import messages
from django.db.models import Count
import bcrypt

def index(request):
    return render(request, 'secrets_app/index.html')

def register(request):
    fname = str(request.POST['first_name'])
    lname = str(request.POST['last_name'])
    email = str(request.POST['email'])
    pwd = request.POST['password'].encode()
    conpwd = request.POST['confirm_password'].encode()
    context = {
    "fname" : fname,
    "lname" : lname,
    "email" : email,
    "pwd" : pwd,
    "conpwd" : conpwd
    }
    if  User.objects.all().filter(email = email):
        messages.add_message(request, messages.INFO, "Email already exists! Please login")
        return redirect('/')
    error = User.objects.validate(context)
    if error:
        for ele in error:
            messages.add_message(request, messages.ERROR, ele)
        return redirect('/')
    else:
        hashedpwd = bcrypt.hashpw(pwd, bcrypt.gensalt())
        user = User.objects.create(first_name = fname, last_name = lname, email = email, password = hashedpwd)
        request.session['uid'] = user.id
        request.session['uname'] = user.first_name
    return render(request, 'secrets_app/hush.html')


def login(request):
    email = str(request.POST['email'])
    pwd = request.POST['password'].encode()
    user = User.objects.all().filter(email = email)
    if  not user:
        messages.add_message(request, messages.INFO, "Email doesn't exist! Please register")
        return redirect('/')
    else:
        if user[0].password != bcrypt.hashpw(pwd, (user[0].password).encode()):
            messages.add_message(request, messages.INFO, "Invalid password")
            return redirect('/')
        else:
            request.session['id'] = user[0].id
            request.session['uname'] = user[0].first_name
    return render(request, 'secrets_app/hush.html')

def process(request):
    if request.method=="GET":
        return redirect('/')
    print "Hello", request.POST
    result = Secret.objects.validate(request.POST['secret'], request.session['id'])
    if result[0]:
        messages.info(request, result[1])
        return redirect('/secrets')
    messages.error(request, result[1])
    return redirect('/secrets')

def secrets(request):
    if checkForLogin(request):
        allsecrets = Secret.objects.all().order_by('-id')[:5]
        context = {
            "secrets" : allsecrets,
            "currentuser" : User.objects.get(id=request.session['id'])
        }
        return render(request, 'secrets_app/hush.html', context)
    else:
        return redirect('/')

def newLike(request, id, sentby):
    print "we are in the new like", id
    result = Secret.objects.newLike(id, request.session['id'])
    if result[0] == False:
        messages.error(request, result[1])
    if sentby == "sec":
        return redirect('/secrets')
    else:
        return redirect('/popular')

def delete(request, id, sentby):
    print "we are in the delete", id
    result = Secret.objects.deleteLike(id, request.session['id'])
    if result[0] == False:
        messages.error(request, result[1])
    if sentby == "sec":
        return redirect('/secrets')
    else:
        return redirect('/popular')

def popular(request):
    if checkForLogin(request):
        allsecrets = Secret.objects.annotate(num_likes=Count('likers')).order_by('-num_likes')
        context = {
            "secret" : allsecrets,
            "currentuser" : User.objects.get(id=request.session['id'])
        }
        return render(request, 'secrets_app/popular.html', context)
    else:
        return redirect('/')

def logout(request):
    request.session.pop('id')
    return redirect('/')

def checkForLogin(request):
    if 'id' not in request.session:
        messages.error(request, "You must login to view the request page", extra_tags='register')
        return False
    return True
