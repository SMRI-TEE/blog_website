from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from base.models import Category,Blog,Comment
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import RegistrationForm,CategoryForm,BlogForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib import messages
from django.http import HttpResponseRedirect
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import urllib, base64
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify

# Create your views here.
def home(request):
    categories = Category.objects.all()
    featured_post = Blog.objects.filter(is_featured=True,status=1)
    posts = Blog.objects.filter(is_featured=False,status=1)
    
    context={
        'categories':categories,
        'featured_post':featured_post,
        'posts':posts,
    }
    return render(request,'home.html',context)

def posts_by_category(request,id):
    # fetching the posts that belongs to the category with id id.
    posts = Blog.objects.filter(status=1,category=id)
    categories = Category.objects.all()
    try : 
        category = Category.objects.get(pk=id)
    except :
        return redirect('home')    
    
    context = {
        'categories':categories,
        'posts':posts,
        'category':category,
    }
    
    return render(request,'posts_by_category.html',context)

# this function is used for displaying a single blog.
def blogs(request,slug):
    single_post = get_object_or_404(Blog,slug=slug,status=1)
    # for displaying comment
    if request.method=='POST':
        comment = Comment()
        comment.user = request.user
        comment.blog = single_post
        comment.comment = request.POST['comment']
        comment.save()
        return HttpResponseRedirect(request.path_info)
    comments = Comment.objects.filter(blog=single_post)
    comment_count = comments.count()
    context = {
        'single_post':single_post,
        'comments':comments,
        'comment_count':comment_count
        
    }
    return render(request,'blogs.html',context)

# search function 
def search(request):
    keyword = request.GET.get('keyword')
    blogs = Blog.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(blog_body__icontains=keyword),status=1)
    # for displaying by short description should use complexquery., we have been using Q.
    
    context = {
        'blogs':blogs,
        'keyword':keyword,
    }
    return render(request,'search.html',context)

def register(request):
    if request.method=="POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register')     
    else :
        form = RegistrationForm()
    context={
        'form':form,
    }
    return render(request,'register.html',context)

# for login functionality 

def login(request):
    # authentication form import then use.
    # builtin form
    if request.method=="POST":
         form = AuthenticationForm(request, request.POST)
         if form.is_valid():
             # getting username and password
             username = form.cleaned_data['username']
             password = form.cleaned_data['password']
             
             user = auth.authenticate(username=username,password=password)
             if user is not None:
                 auth.login(request,user)
                 return redirect('dashboard')
                 
    else:
        form = AuthenticationForm()
    context={
        'form':form,
       
    }
    return render(request,'login.html',context)

def logout(request):
    auth.logout(request)
    return redirect('home')

# for dashboard 
@login_required(login_url='login')
def dashboard(request):
    total_categories = Category.objects.count()
    total_posts = Blog.objects.count()  # total posts

    # Blog count per category
    category_data = Category.objects.annotate(
        total_posts=Count('blog')
    )

    labels = []
    sizes = []

    for category in category_data:
        labels.append(category.category_name)
        sizes.append(category.total_posts)

    # 🔹 Create pie chart using matplotlib
    plt.figure(figsize=(6,6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Blogs by Category')
    plt.tight_layout()

    # 🔹 Convert plot to image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    context = {
        'total_categories': total_categories,
        'total_posts': total_posts, 
        'chart': graphic,
    }

    return render(request, 'dashboard.html', context)

def category_view(request):   
    return render(request,'categories.html')

def add_categories(request):
    if request.method=="POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            if Category.objects.filter(category_name__iexact=category_name).exists():
                messages.error(request, "Category already exists.")
            else:
                form.save()
                return redirect('categories')     
    
    form = CategoryForm()
    context = {
        'form': form,
       
    }
    return render(request,'add_categories.html',context)

def edit_categories(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')  
    else:
        form = CategoryForm(instance=category)

    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'edit_categories.html', context)

def delete_categories(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('categories')

def post_view(request):
    posts = Blog.objects.all()
    return render(request,'posts.html',{'posts':posts})

def add_posts(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)

        if form.is_valid():
            title = form.cleaned_data['title']

            if Blog.objects.filter(title__iexact=title).exists():
                messages.error(request, "Title already exists.")
            else:
                post = form.save(commit=False)
                post.author = request.user
                post.slug = slugify(title)
                post.save()
                return redirect('posts')

    else:
        form = BlogForm()

    return render(request, 'add_posts.html', {'form': form})


def edit_posts(request, pk):
    posts = get_object_or_404(Blog, pk=pk)

    if request.method == "POST":
        form = BlogForm(request.POST, instance=posts)
        if form.is_valid():
            form.save()
            return redirect('posts')  
    else:
        form = BlogForm(instance=posts)

    context = {
        'form': form,
        'posts': posts,
    }
    return render(request, 'edit_posts.html', context)


def delete_posts(request, pk):
    posts = get_object_or_404(Blog, pk=pk)
    posts.delete()
    return redirect('posts')

def users(request):
    users = User.objects.all()
    context = {
        'users':users
    }
    return render(request,'users.html',context)


