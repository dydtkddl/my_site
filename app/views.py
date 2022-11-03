from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
# Create your views here.
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
def home(request):
    articlelist=Article.objects.filter()
    context = {
        'articlelist' : articlelist
    }
    return render(request, 'home.html', context)

def signup(request):
    if request.method =='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')
        phone_number = request.POST.get('phone_number')
        User(name= name, email = email, pwd = pwd, phone_number =phone_number ).save()
        return redirect('/app/home/')
    return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')
        try:
            user = User.objects.get(email = email, pwd = pwd)
            name = user.name
            request.session['email'] = email
            request.session['name'] = name
        except:
            return redirect('/app/signin/')
        return redirect('/app/home/')
    return render(request, 'signin.html')

def signout(request):
    print(request.session.get('email'))
    request.session.flush()
    return redirect('/app/home/')


def article_list(request):
    articlelist = Article.objects.all()
    return render(request , 'articlelist.html', { 'articlelist':articlelist})

def upload(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        title = request.POST.get('title')
        time = datetime.datetime.now().strftime('%Y-%m-%d')
        user_email = request.session['email']
        user = User.objects.get(email = user_email)
        article = Article(contents = content, title = title, time=time, user = user)
        article.save()
        id = article.id
        return redirect('/app/detail/%s' %id)
        
    try:
        # print(request.session['email'])
        # print(request.session['name'])
        email = request.session['email']
        name = request.session['name']
        categorys = Category.objects.all()
        # print(1)
        user = User.objects.get(email = email, name = name)
        return render(request, 'upload.html', {'categorys' : categorys})
    except:
        return redirect('/app/signin/') 
def detail(request, id):
    article = Article.objects.get(id = id)
    title = article.title
    content = article.contents
    time = article.time

    return render(request, 'detail.html', context = { 'title':title, 'content':content, 'time':time })

def mypage(request):
    email = request.session['email']
    user = User.objects.get(email=email)
    myarticles = user.article_set.all()
    return render(request, 'mypage.html', {'myarticles' : myarticles})
# def modify(request):
#     return

# def delete(request):
#     return
import json
@csrf_exempt
def makecategory(request):
    if request.method == 'POST':
        name = json.loads(request.body)
        # name_list = json.load(name)
        # print(name)
        # print(1)
        if Category.objects.filter(name = name['category_name']):
            dic ={'response':'이미 동일한 이름이 있습니다.'}
            return JsonResponse(dic)
        else:
            Category(name = name['category_name']).save()
            dic ={'response':'반영되었습니다'}
            return JsonResponse(dic)
    else:
        return HttpResponse('go_on_post!')
def category_list(request):
    category_list = Category.objects.all()
    data = []
    for i in category_list:
        i=model_to_dict(i)
        data.append(i)
    print(data)
    return JsonResponse(data, safe= False )