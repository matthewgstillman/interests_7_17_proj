from django.shortcuts import render, redirect
from .models import User, Interest
from django.contrib import messages
from django.db.models import Count

# Create your views here.

def register(request):
    #print request.POST
    if request.method == 'POST':
        messages = User.objects.register(request.POST)
        #Above line might be postData
    if not messages:
        print "No messages! Success!"
        # fetch user id and name via email
        user_list = User.objects.all().filter(username=request.POST['username'])
        request.session['id'] = user_list[0].id
        request.session['name'] = user_list[0].first_name
        request.session['username'] = user_list[0].username
        return redirect('/add')
    else:
        request.session['messages'] = messages
        print messages
    return redirect('/')

def login(request):
    users = User.objects.all()
    if request.method == 'POST':
        messages = User.objects.login(request.POST)
    if not messages:
        print "No messages! Success!"
        user_list = User.objects.all().filter(username=request.POST['username'])
        request.session['id'] = user_list[0].id
        request.session['name'] = user_list[0].first_name
        return redirect('/add')
    else:
        request.session['messages'] = messages
        return redirect('/')

def index(request):
    users = User.objects.all()
    for user in users:
        print user.username
    if 'messages' in request.session:
        context={
            'messages': [],
            'users': users
        }
    return render(request, 'interests_7_17/index.html')

def add(request):
    context={
        'interests': Interest.objects.all(),
        'users': User.objects.all()
    }
    return render(request, 'interests_7_17/add.html', context)

def add_info(request):
    # user = User.objects.get(id=request.session['id'])
    user = User.objects.get(username=request.POST['username'])
    interest = Interest.objects.filter(interest=request.POST['interest'])
    validation = Interest.objects.validate(request.POST)
    # if not validation:
    #     print "Validation fucked"
    #     return redirect('/add')
    if not interest:
        interest = Interest.objects.create(interest=request.POST['interest'])
    else:
        interest = interest[0]
    print interest
    add_interest = interest.users.add(user)
    return redirect('/users')

def users(request):
    users = User.objects.all()
    print users
    interests = Interest.objects.all()
    context={
        'users': users,
    }
    postData = {
        'interests': interests
    }
    return render(request, 'interests_7_17/users.html', context)

def show(request, id):
    user = User.objects.get(id=id)
    username = User.objects.get(id=id)
    user_interests = Interest.objects.filter(users__id=id)
    interests = user.user_interests.all()
    all_interests = Interest.objects.all()
    context = {
        'username': username,
        'user_interests': user_interests,
        'interests': interests,
        'id': id,
        # 'interest_id': interest_id
    }
    print context
    return render(request, 'interests_7_17/show.html', context)

def all_interests(request):
    interests = Interest.objects.all()
    context = {
        'interests': interests
    }
    return render(request, 'interests_7_17/all_interests.html', context)

def delete(request, id):
    interest = Interest.objects.get(id=id)
    result = Interest.objects.delete_interest(id)
    context = {
        'interest': interest
    }
    return redirect('/all_interests')
