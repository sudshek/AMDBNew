"""AMDB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from Users.views import get_user
from django.conf.urls import url
from django.contrib import admin
from Users.views import create_user
from Users.views import login_user
from Users.views import create_movie
from Users.views import review_movie
from Users.views import get_movie


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^user/',get_user),
    url(r'^create/users/',create_user),
    url(r'^login/',login_user),
    url(r'^movie/create/',create_movie),
    url(r'^movie/review/',review_movie),
    url(r'^movie/list/',get_movie)

]
