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
        category = request.POST.get('category')
        category = Category.objects.get(name = category)
        article = Article(contents = content, title = title, time=time, user = user,category=category)
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
    id = article.id
    title = article.title
    content = article.contents
    time = article.time
    category = article.category.name
    return render(request, 'detail.html', context = { 'id':id, 'title':title, 'content':content, 'time':time ,'category':category})

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
        print(i)
        i=model_to_dict(i)
        data.append(i)
    print(data)
    return JsonResponse(data, safe= False )
@csrf_exempt
def remove_category(request):
    list_ = []
    if request.method == 'POST':
        checked = json.loads(request.body)
        checked = list(checked['checked'].values())
        print(checked)
        for i in checked:
            Category.objects.get(name = i).delete()
        return HttpResponse('hi')
        # print(checked['checked'])
        # list_.append(checked['checked'])        
        # return JsonResponse(list_, safe=False)
    return HttpResponse('back')

def call_category(request):
    category = request.GET.get('category')
    category = Category.objects.get(name = category)
    call_articles = Article.objects.filter(category = category)
    context = {
        'articles':call_articles
    }
    return render(request, 'filtered_articles.html',context)
@csrf_exempt
def modify_article(request):
    if request.method=='POST':
        all_content = json.loads(request.body)
        id = all_content['id']
        title = all_content['title']
        category = all_content['category']
        content = all_content['content']
        article = Article.objects.get(id = id)
        article.title = title
        category = Category.objects.get(name = category)
        article.category= category
        article.contents = content
        article.time = datetime.datetime.now().strftime('%Y-%m-%d')
        article.save()
        dic ={
            'id':id,
            'title':title,
            'category':category,
            'content':content
            }
        print(id, title, category, content)
        return HttpResponse(dic)
    else:
        return HttpResponse('fail')
@csrf_exempt
def remove_article(request):
    if request.method=='POST':
        print(json.loads(request.body))
        article_id = json.loads(request.body)['id']
        article = Article.objects.get(id = article_id)
        article.delete()
        return HttpResponse('ok')
    else:
        return HttpResponse('fail')