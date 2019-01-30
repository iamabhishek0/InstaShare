from django.shortcuts import render
from django.views import generic
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate
from django.db.models import Q
from django.shortcuts import render,redirect,HttpResponseRedirect

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django import forms
from .forms import UserRegistrationForm,PostForm


from .models import Post, User


# from templates.posts import post_form.html

def post_list(request):

    blog_post = User.objects.all()
    query = request.GET.get("q")
    if query:
        blog_post = blog_post.filter(Q(title__icontains=query)|
                                    Q(content__icontains=query)).distinct()
    paginator = Paginator(blog_post, 3)  # Show 25 contacts per page

    page = request.GET.get('page')
    all_posts = paginator.get_page(page)


    return render(request, 'posts/index.html', {'all_posts': all_posts})


class Detailview(generic.DetailView):
    model = Post
    template_name = 'posts/detail.html'




class PostCreate(CreateView):

    # def get(self, request):
    #     if not request.user.is_staff or not request.user.is_superuser:
    #         raise Http404
    #     return render(request,'posts/')
    model = Post
    fields = ['title', 'content', 'post_image']
    # instance = form.save(commit=False)
    # instance.user = request.user
    # instance.save()
    # template_name = 'blog/post_form.html'

    success_url = reverse_lazy('post:index')

    # def get(self, request):
    #     if not request.user.is_staff or not request.user.is_superuser:
    #         raise Http404

# def create(request):
#     form = PostForm(request.POST or None)
#     if form.is_valid():
#         instance = form.save(commit=False)
#         instance.user = request.user
#         instance.save()
#         return HttpResponseRedirect('/home')
#     return render(request,'posts/create.html',{'form':form})

class PostUpdate(UpdateView):
    model = Post
    fields = ['title', 'content', 'post_image']

class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('post:index')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email =  userObj['email']
            password =  userObj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username = username, password = password)
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')
    else:
        form = UserRegistrationForm()
    return render(request, 'posts/register.html', {'form' : form})


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated



class HelloView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)