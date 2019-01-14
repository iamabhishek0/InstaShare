from django.shortcuts import render
from django.views import generic
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator

from django.db.models import Q
from django.shortcuts import render,redirect,HttpResponseRedirect


from .models import Post


# from templates.posts import post_form.html

def post_list(request):

    blog_post = Post.objects.all()
    query = request.GET.get("q")
    if query:
        blog_post = blog_post.filter(Q(title__icontains=query)|
                                    Q(content__icontains=query)).distinct()
    paginator = Paginator(blog_post, 2)  # Show 25 contacts per page

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
    # template_name = 'blog/post_form.html'

    success_url = reverse_lazy('post:index')

    # def get(self, request):
    #     if not request.user.is_staff or not request.user.is_superuser:
    #         raise Http404

class PostUpdate(UpdateView):
    model = Post
    fields = ['title', 'content', 'post_image']

class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('post:index')