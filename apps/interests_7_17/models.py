from __future__ import unicode_literals

from django.db import models
import md5
import bcrypt
import os, binascii

import re
NAME_REGEX =re.compile('^[A-z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class UserManager(models.Manager):
    def login(self, postData):
        messages = []
        # first_name = postData['first_name']
        # if len(str(first_name)) > 2:
        #     messages.append("First Name must be longer than 2 characters! What kind of pathetic first name is that, bruh?")
        # last_name = postData['last_name']
        # if len(str(last_name)) < 2:
        #     messages.append("Last Name must be longer than 2 characters! What kind of pathetic  last name is that, bruh?")
        username = postData['username']
        if len(str(username)) < 5:
            messages.append("Username must be longer than 5 characters, bruh!")
        password = postData['password']
        if len(str(password)) < 8:
            messages.append("Password must be 8 characters or longer, bruh! This shit is getting pathetic!")
        # pw_confirm = postData['pw_confirm']
        # if password != pw_confirm:
        #     messages.append("Passwords must match Bruh! If you're trying to be some sort of computer hacker, you're not very good at it!")
        # if User.objects.filter(username=username):
        #     #encode the registered user's password from database to a specific format
        #     db_pw = User.objects.get(username=username).password.encode()
        #     #Compare the password with the password in database
        #     if not bcrypt.checkpw(login_pw, db_pw):
        #         messages.append("Password is Incorrect")
        #     else:
        #         messages.append("Username has already been registered!")
            return messages

    def register(self, postData):
        print "register process"
        messages = []
        first_name = postData['first_name']
        if len(str(first_name)) < 1:
            messages.append("Error! First name must not be blank!")
        if len(str(first_name)) < 2:
            messages.append("Error! First name must be at least 2 characters long!")

        last_name = postData['last_name']
        if len(str(last_name)) < 1:
            messages.append("Error! Last name must not be blank!")
        if len(str(last_name)) < 2:
            messages.append("Error! Last name must be at least 2 characters long!")

        username = postData['username']
        if len(str(username)) < 2:
            messages.append("Error! Email must be at least 2 characters long!")

        password = postData['password']
        if len(str(password)) < 1:
            messages.append("Error! Password must not be blank!")
        if len(str(password)) < 8:
            messages.append("Error! Password must be at least 8 characters long!")

        pw_confirm = postData['pw_confirm']
        if pw_confirm != password:
            messages.append("Error! Passwords must match!")

        user_list = User.objects.filter(username=username)
        for user in user_list:
            print user.username
        if user_list:
            messages.append("Error! Username is already in the system!")
        if not messages:
            print "No messages"
            password = password.encode()
            salt = bcrypt.gensalt()
            hashed_pw = bcrypt.hashpw(password, salt)
            # password = password
            print "Create User"
            print hashed_pw
            User.objects.create(first_name=first_name, last_name=last_name, username=username, password=hashed_pw)
            print hashed_pw
            print User.objects.all()
            return None
        return messages

class InterestManager(models.Manager):
    def validate(self, postData):
        username = postData['username']
        if len(str(username)) < 8:
            return (False, "Username not quite long enough! Try again bruh!")
        interest = postData['interest']
        if len(str(interest)) < 8:
            return (False, "Interest not long enough to be taken seriously!")

    def delete_interest(self, interest_id):
        try:
            interest = self.get(id=interest_id)
        except:
            return(False, "This interest was not found in the database")
        interest.delete()
        return(True, "Interest Deleted")

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    pw_confirm = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __unicode__(self):
        return "id: " + str(self.id) + ", First Name: " + str(self.first_name) + ", Last Name: " + str(self.last_name) + ", Username: " + str(self.username)

class Interest(models.Model):
    interest = models.CharField(max_length= 50)
    users = models.ManyToManyField(User, related_name="user_interests")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = InterestManager()

    def __unicode__(self):
        return "id: " + str(self.id) + ", interest: " + self.interest
