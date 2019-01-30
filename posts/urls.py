from posts import views
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as auth_views
# from django.mysicore import views as core_views


from .views import (
	post_list,

	)
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

app_name='post'

urlpatterns = [

    #
    path("", post_list, name = "index"),

    path('hello/', views.HelloView.as_view(), name='hello'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    # path("", views.search(), name = "search"),

    path('<int:pk>/', views.Detailview.as_view(), name = "detail"),

    path('add/', login_required(views.PostCreate.as_view()), name='post-add'),

    path('register/', views.register, name = 'register'),

    path('post/<int:pk>/', login_required(views.PostUpdate.as_view()), name='post-update'),

    path('post/<int:pk>/delete/', login_required(views.PostDelete.as_view()), name='post-delete'),
]