
from django.views import generic
from django.contrib import messages
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django import forms
from .forms import UserRegistrationForm,PostForm
from .models import Post




def post_list(request):

    blog_post = Post.objects.all()
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


def post_create(request):


    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()

        messages.success(request, "Successfully Created")
        return HttpResponseRedirect('/')
    context = {
        "form": form,
    }
    return render(request, "posts/post_form.html", context)


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


# ignore it

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated



class HelloView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)