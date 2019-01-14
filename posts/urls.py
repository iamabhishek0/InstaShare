from posts import views
from django.urls import path
from .views import (
	post_list,

	)
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

app_name='post'

urlpatterns = [

    #
    path("", post_list, name = "index"),

    # path("", views.search(), name = "search"),

    path('<int:pk>/', views.Detailview.as_view(), name = "detail"),

    path('add/', login_required(views.PostCreate.as_view()), name='post-add'),

    path('post/<int:pk>/', login_required(views.PostUpdate.as_view()), name='post-update'),

    path('post/<int:pk>/delete/', login_required(views.PostDelete.as_view()), name='post-delete'),
]