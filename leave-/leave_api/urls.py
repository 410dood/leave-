"""todo_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
#
# from django.conf.urls import url
# from django.urls import include, path
# from django.contrib import admin
# from django.views.generic import TemplateView
#
# from dests import endpoints
#
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include('dests.urls')),
#     url(r'^admin/', admin.site.urls),
#     url(r'^', TemplateView.as_view(template_name="index.html")),
# ]



from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from dests import endpoints
# from dests import views


urlpatterns = [
    # path('', views.ListDest.as_view()),
    # path('<int:pk>/', views.DetailDest.as_view()),
    path('api/', include(endpoints)),
    path('admin/', include(endpoints)),
    path('api/auth/', include('knox.urls')),
    re_path('^', TemplateView.as_view(template_name="index.html")),
]
