from django.shortcuts import render
  
# relative import of forms
from .models import GeeksModel
from .forms import GeeksForm
  
  
def create_view(request):
    # dictionary for initial data with 
    # field names as keys
    context ={}
  
    # add the dictionary during initialization
    form = GeeksForm(request.POST or None)
    if form.is_valid():
        form.save()
          
    context['form']= form
    

    return render(request, "QR/newCV.html", context)