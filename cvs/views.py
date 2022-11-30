from django.shortcuts import render
  
# relative import of forms
from .models import GeeksModel
from .forms import GeeksForm
  
  
def index(request):
   if request.method == 'POST':
      var = request.POST['describe']