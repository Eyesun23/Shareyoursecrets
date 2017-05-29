from __future__ import unicode_literals
from django.db import models
import re


class UserManager(models.Manager):
    def validate(self, data):
        error = []
        emailreg = '[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+'
        print "Inside validate"
        if len(data['fname']) < 2 or not str.isalpha(data['fname']):
            print "inside if"
            error.append("Invalid First Name")
        if len(data['lname']) < 2 or not str.isalpha(data['lname']):
            error.append("Invalid Last Name")
        if  not re.search(emailreg, data['email']):
            error.append("Invalid Email")
        if len(data['pwd']) < 4:
            error.append("Minimum of 4 characters required for password")
        if data['pwd'] != data['conpwd']:
            error.append("Password doesn't match")
        return error

class SecretManager (models.Manager):
    def validate(self, dataSecret, userid):
        if len(dataSecret)<4:
            return(False, "secrets must be at least four characters longs")
        try:
            currentuser = User.objects.get(id=userid)
            self.create(secret=dataSecret, author=currentuser)
            return (True, "Your secret is safe")
        except:
            return(False, "We could not create this secret")

    def newLike(self, secretid, userid):
        try:
            secret = self.get(id=secretid)
        except:
            return(False, "this is not found in our secret database")
        user = User.objects.get(id=userid)
        if secret.author == user:
            return(False, "Shame on you, you shouldn't like your own secrets")
        secret.likers.add(user)
        return (True, "You liked this secret!")
    def deleteLike (self, secretid, userid):
        try:
            secret = self.get(id=secretid)
        except:
            return(False, "this is not found in our secret database")
        user = User.objects.get(id=userid)
        if secret.author != user:
            return(False, "Shame on you, you shouldn't delete secrets that are not yours")
        secret.delete()
        return(True, "Secret deleted")

class User(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length= 40)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Secret(models.Model):
    secret = models.CharField(max_length=400)
    author = models.ForeignKey(User)
    likers = models.ManyToManyField(User, related_name="likedsecrets")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SecretManager()
