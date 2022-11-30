"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import newCV
from .views import myCv
from .views import qr
from .views import qaa
from .views import index
from .views import validate
from .views import downloadFile
from .views import pdf_report_create
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('pages.urls')),  # new
    # # path('cv/', newCV),
    path('myCV/', myCv),
    path('qr/', qr),
    path('qaa/', qaa),
    path('downloadFile/', downloadFile),
    # path("",include("sendemail.urls"))
    path('cv/', index, name = 'index'), #index= padina care se completeaza
    path('cv/validate', validate, name = 'validate'),
    path('cv/validate/pdf', pdf_report_create, name = 'pdf_report_create')
]
