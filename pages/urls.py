# pages/urls.py
from django.urls import path
from .views import newCV
from .views import myCv
from .views import qr
from .views import qaa

from .views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('cv/',newCV ),
     path('myCV/', myCv),
     path('qr/', qr),
     path('qaa/', qaa),
    
]