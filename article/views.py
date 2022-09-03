from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from PIL import Image

# Create your views here.
def home(request):

    if request.user.is_authenticated:

        current_user = request.user
        connected_user_linked = User_article.objects.get(user_linked=current_user)
        current_user_categories = []
        for i in connected_user_linked.categories_user.all():
            current_user_categories.append(i.id)

        all_categrories = Categories.objects.filter(id__in=current_user_categories)
        try:
            if request.method == "POST":
                if 'ARTICLE' in request.POST:
                    title = request.POST["TITLE"]
                    year = request.POST["YEAR"]
                    if year != '' and title != '':
                        categories_names = [x.title for x in all_categrories]
                        categories_ids = []
                        for x in categories_names:
                            categories_ids.append(int(request.POST.get(x))) if request.POST.get(x) else print('no')
                        article = Article.objects.create(
                            title = str(title),
                            year_created = year
                        )
                        connected_user_linked.articles_user.add(article)
                        article.save()
                        for category_id in categories_ids:
                            article.categories.add(Categories.objects.get(id=category_id))
                            article.save()
                    else:
                        pass
                elif 'CATEGORY' in request.POST:
                    title = request.POST["TITLE"]
                    if title == '':
                        pass
                    else:
                        category = Categories.objects.create(
                            title = title
                        )
                        category.save()

                        connected_user_linked.categories_user.add(category)
                
                elif 'SEARCH_BY_CATEGORY' in request.POST:
                    article_name = request.POST['article_name']
                    catgories_by_search = [x.title for x in all_categrories]
                    categories_ids_search = []
                    for x in catgories_by_search:
                        categories_ids_search.append(str(request.POST.get(x))) if request.POST.get(x) else print('no')
                    if categories_ids_search == [] and article_name == "":
                        pass
                    else:
                        return redirect('get_article/{0}-{1}'.format(("+".join(categories_ids_search)), article_name))
            
                elif 'CHANGE_USERNAME' in request.POST:
                    if request.POST['USERNAME'] != '' and len(request.POST['USERNAME']) >= 4:
                        connected_user_linked.username = request.POST['USERNAME']
                    if len(request.FILES) != 0:
                        image = Image.open(request.FILES['PROFILE'])
                        width, height = image.size
                        if width == height:
                            connected_user_linked.article_profile_pic = request.FILES['PROFILE']
                    connected_user_linked.save()
        except:
            pass
                
        current_user_articles = []
        for i in connected_user_linked.articles_user.all():
            current_user_articles.append(i.id)
        
        current_user_categories = []
        for i in connected_user_linked.categories_user.all():
            current_user_categories.append(i.id)

        all_categrories = Categories.objects.filter(id__in=current_user_categories)

        context = {'user':connected_user_linked,'categories':all_categrories, 'articles':Article.objects.filter(id__in=current_user_articles).order_by('year_created')}
        return render(request, 'article/home.html',context)
    
    return(redirect('signup'))

@login_required
def delet_article(request, article_id):
    current_user = request.user
    connected_user_linked = User_article.objects.get(user_linked=current_user)

    current_articles = []
    for i in connected_user_linked.articles_user.all():
        current_articles.append(i.id)

    all_articles = Article.objects.filter(id__in=current_articles)
    article = all_articles.filter(id=article_id.split("+")[0])
    article.delete()
    if '+' not in article_id:
        return redirect('home')
    return redirect('/collection/{0}'.format(article_id.split("+")[1]))
    
@login_required
def delet_category(request, category_id):
    current_user = request.user
    connected_user_linked = User_article.objects.get(user_linked=current_user)

    current_categories = []
    for i in connected_user_linked.categories_user.all():
        current_categories.append(i.id)

    all_categories = Categories.objects.filter(id__in=current_categories)
    category = all_categories.filter(id=category_id.split("+")[0])
    category.delete()

    if '+' not in category_id:
        return redirect('home')
    return redirect('/collection/{0}'.format(category_id.split("+")[1]))

@login_required
def get_article(request, article_ids):
    current_user = request.user
    connected_user_linked = User_article.objects.get(user_linked=current_user)
    
    current_user_articles = []
    for i in connected_user_linked.articles_user.all():
        current_user_articles.append(i.id)

    articles = Article.objects.filter(id__in=current_user_articles)


    list_article_filter = []
    list_articles_by_category_ids = str(str(article_ids).split('-')[0]).split('+')
    if str(article_ids).split('-')[0] == '':
        for i in articles:
            if ''.join(str(article_ids).split('-')[1]) in i.title:
                list_article_filter.append(i.id)

    elif str(article_ids).split('-')[1] == '':
        for article in articles:
            for i in article.categories.all():
                for j in list_articles_by_category_ids:
                    if i.id == int(j):
                        list_article_filter.append(article.id)

    elif str(article_ids).split('-')[1] == '' and str(article_ids).split('-')[0] == '':
        pass

    else:
        for article in articles:
            for i in article.categories.all():
                for j in list_articles_by_category_ids:
                    if i.id == int(j):
                        list_article_filter.append(article.id)

        for i in articles:
            if ''.join(str(article_ids).split('-')[1]) in i.title and i.id not in list_article_filter:
                list_article_filter.append(i.id)
    
    if article_ids.count('-') == 2:
        collection_id = article_ids.split('-')[2]
        collection = Collections.objects.get(id=collection_id)
        collection_list = []
        for i in collection.articles.all():
            if i.id in list_article_filter:
                collection_list.append(i.id)
        get_articles_by_c = Article.objects.filter(id__in=collection_list)
        return render(request, 'article/get_article.html', {'articles':get_articles_by_c.order_by('year_created'), 'return_collection':True, 'collection':collection})
    else:
        get_articles_by_c = Article.objects.filter(id__in=list_article_filter)
        return render(request, 'article/get_article.html', {'articles':get_articles_by_c.order_by('year_created'), 'return_collection':False})

def signup(request):
    if request.method == "POST":
        name = request.POST["USERNAME"]
        confirm_pass = request.POST["PASSWORD"]
        password = request.POST["CONFIRM"]
        email = request.POST["EMAIL"]
        if email != '' and name != '' and password != "":
            if confirm_pass == password and len(str(password)) >= 5:
                user = User.objects.create_user(username = email, password = password)
                user.save()
                user_article = User_article.objects.create(
                    username = name,
                    user_linked = user
                )

                user_article.save()
                article_example = Article.objects.create(
                    title="מאמר דוגמה",
                    year_created=2022
                )

                article_example.save()
                category_example = Categories.objects.create(
                    title = 'קטגוריה דוגמה'
                )

                category_example.save()

                article_example.categories.add(category_example)
                user_article.categories_user.add(category_example)
                user_article.articles_user.add(article_example)

                user = authenticate(request, username=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
            else:
                pass
        else:
            pass
    return render(request, 'article/signup.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['EMAIL']
        password = request.POST['PASSWORD']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'article/login.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect('signin')

@login_required
def collection_mg(request):
    current_user = request.user
    connected_user_linked = User_article.objects.get(user_linked=current_user)
    
    if request.method == 'POST':
        if 'COLLECTION' in request.POST:
            new_collection = Collections.objects.create(
                title = request.POST['TITLE']
            )
            new_collection.save()
            new_collection.participants.add(connected_user_linked)
            new_collection.admins.add(connected_user_linked)
            new_collection.save()

        elif 'CHANGE_USERNAME' in request.POST:
            if request.POST['USERNAME'] != '' and len(request.POST['USERNAME']) >= 4:
                connected_user_linked.username = request.POST['USERNAME']
            if len(request.FILES) != 0:
                image = Image.open(request.FILES['PROFILE'])
                width, height = image.size
                if width == height:
                    connected_user_linked.article_profile_pic = request.FILES['PROFILE']
            connected_user_linked.save()

    all_collections = Collections.objects.all()
    collections_user = []
    for i in all_collections:
        if (connected_user_linked in i.participants.all()):
            collections_user.append(i.id)

    all_user_collections = Collections.objects.filter(id__in=collections_user)

    all_user_collections_categories = []
    for i in all_user_collections:
        for j in i.categories.all():
            all_user_collections_categories.append(j.id)
    categories_in_all_collections =  Categories.objects.filter(id__in=all_user_collections_categories)
 
    context = {'collections':all_user_collections, 'user':connected_user_linked, 'categories':categories_in_all_collections}
    return render(request, 'article/collection.html',context)

@login_required
def delete_collection(request, collection_id):
    collection = Collections.objects.get(id=collection_id)
    collection.delete()
    return redirect('collection_mg')

@login_required
def collection_home(request, collection_id):
    if request.user.is_authenticated:
        collection = Collections.objects.get(id=collection_id)
        current_user = request.user
        connected_user_linked = User_article.objects.get(user_linked=current_user)
        current_collection_categories = []
        for i in collection.categories.all():
            current_collection_categories.append(i.id)

        all_categrories = Categories.objects.filter(id__in=current_collection_categories)
        try:
            if request.method == "POST":
                if 'ARTICLE' in request.POST:
                    title = request.POST["TITLE"]
                    year = request.POST["YEAR"]
                    if year != '' and title != '':
                        categories_names = [x.title for x in all_categrories]
                        categories_ids = []
                        for x in categories_names:
                            categories_ids.append(int(request.POST.get(x))) if request.POST.get(x) else print('no')
                        article = Article.objects.create(
                            title = str(title),
                            year_created = year
                        )
                        connected_user_linked.articles_user.add(article)
                        collection.articles.add(article)
                        article.save()
                        for category_id in categories_ids:
                            article.categories.add(Categories.objects.get(id=category_id))
                            collection.categories.add(Categories.objects.get(id=category_id))
                            article.save()
                    else:
                        pass
                elif 'CATEGORY' in request.POST:
                    title = request.POST["TITLE"]
                    if title == '':
                        pass
                    else:
                        category = Categories.objects.create(
                            title = title
                        )
                        category.save()

                        collection.categories.add(category)
                        connected_user_linked.categories_user.add(category)
                
                elif 'SEARCH_BY_CATEGORY' in request.POST:
                    article_name = request.POST['article_name']
                    catgories_by_search = [x.title for x in all_categrories]
                    categories_ids_search = []
                    for x in catgories_by_search:
                        categories_ids_search.append(str(request.POST.get(x))) if request.POST.get(x) else print('no')
                    if categories_ids_search == [] and article_name == "":
                        pass
                    else:
                        return redirect('get_article/{0}-{1}-{2}'.format(("+".join(categories_ids_search)), article_name, request.POST['SEARCH_BY_CATEGORY']))
            
                elif 'CHANGE_USERNAME' in request.POST:
                    if request.POST['USERNAME'] != '' and len(request.POST['USERNAME']) >= 4:
                        connected_user_linked.username = request.POST['USERNAME']
                    if len(request.FILES) != 0:
                        image = Image.open(request.FILES['PROFILE'])
                        width, height = image.size
                        if width == height:
                            connected_user_linked.article_profile_pic = request.FILES['PROFILE']
                    connected_user_linked.save()
                
                elif 'ADD_USER_PARTICIPANT' in request.POST:
                    username_and_src = request.POST['USERNAME']
                    try:
                        user_to_add = User_article.objects.get(username=username_and_src)
                        current_collection = Collections.objects.get(id=request.POST['ADD_USER_PARTICIPANT'])
                        current_collection.participants.add(user_to_add)
                        current_collection.readers.add(user_to_add)
                        current_collection.save()

                        return('/collection/{0}'.format(username_and_src.split('+')[1]))
                    except:
                        pass

        except:
            pass
                
        current_collection_articles = []
        for i in collection.articles.all():
            current_collection_articles.append(i.id)
        
        current_collection_categories = []
        for i in collection.categories.all():
            current_collection_categories.append(i.id)

        all_categrories = Categories.objects.filter(id__in=current_collection_categories)

        if collection.readers.filter(user_linked=request.user).exists():
            role_choose = 1
        elif collection.writers.filter(user_linked=request.user).exists():
            role_choose = 2
        elif collection.admins.filter(user_linked=request.user).exists():
            role_choose = 3

        context = {
            'role':role_choose,
            'collection':collection,
            'user':connected_user_linked,
            'categories':all_categrories,
            'articles':Article.objects.filter(id__in=current_collection_articles).order_by('year_created')}
        
        return render(request, 'article/collection_home.html',context)
    
    return(redirect('signup'))

@login_required
def remove_participant(request, collection_id):
    collection = Collections.objects.get(id=collection_id.split('+')[1])
    user_id = collection_id.split('+')[0]
    user_to_remove = User_article.objects.get(id=user_id)
    collection.participants.remove(user_to_remove)
    collection.save()
    return redirect('/collection/{0}'.format(collection_id.split('+')[1]))

@login_required
def change_role(request, role_number):
    user = User_article.objects.get(id=role_number.split('+')[0])
    collection = Collections.objects.get(id=role_number.split('+')[1])
    role = role_number.split('+')[2]

    collection.readers.remove(user)

    collection.writers.remove(user)

    collection.admins.remove(user)

    collection.save()

    if role == "1":
        print(1)
        collection.readers.add(user)
    elif role == "2":
        collection.writers.add(user)
    elif role == "3":
        collection.admins.add(user)
    collection.save()
    return(redirect('/collection/{0}'.format(collection.id)))