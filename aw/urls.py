"""
URL configuration for aw project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from core.views import home, file_content, update_compilation_options, add_file, add_directory, update_standard, update_processor, update_optimization, compile_and_update, delete_directory_view, delete_file_view

from django.urls import path
#from . import views
from core.views import *
from core.forms import *

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home, name='home'),
    #path('get_directories/', directory_tree, name='directory_tree'),
    path('admin/', admin.site.urls),
    path('file/<int:file_id>/', file_content, name='file_content'),
    path('update_compilation_options/<int:file_id>/', update_compilation_options, name='update_compilation_options'),
    path('add_file/', add_file, name='add_file'),
    path('add_directory/', add_directory, name='add_directory'),
    path('update_standard/', update_standard, name='update_standard'),
    path('update_optimization/', update_optimization, name='update_optimization'),
    path('update_processor/', update_processor, name='update_processor'),
    path('compile_and_update/<int:file_id>/', compile_and_update, name='compile_and_update'),
    path('delete_file/', delete_file_view, name='delete_file'),
    path('delete_directory/', delete_directory_view, name='delete_directory'),
    path("login/", MyLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page='core:login'), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('update_file_content/', update_file_content, name='update_file_content'),
    # other urls...
    #path('add_file_or_directory/', FileCreateView.as_view(), name='add_file'),
]
