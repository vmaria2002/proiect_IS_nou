from django.shortcuts import render

# Create your views here.
# pages/views.py
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render
import qrcode
import qrcode.image.svg
import smtplib
from io import BytesIO

def newCV(request):
    return render(request, 'QR/newCV.html')  

def myCv(request):
     return render(request, 'QR/MyCV.html')  

def qr(request):
     context = {}
     if request.method == "POST":
          factory = qrcode.image.svg.SvgImage
          img = qrcode.make(request.POST.get("qr_text",""), image_factory=factory, box_size=20)
          stream = BytesIO()
          img.save(stream)
          context["svg"] = stream.getvalue().decode()

     return render(request, "QR/QRcode.html")

def qaa(request):
     smtpr=smtplib.SMTP("smtp.gmail.com", 587) 
     smtpr.ehlo()
     smtpr.starttls()
     smtpr.login("maria.vasilache02@gmail.com", "qgrqmaoreadfcszp")
     smtpr.sendmail("maria.vasilache02@gmail.com", "maria.vasilache02@gmail.com","subject:hii\n" )
     smtpr.quit()
     return render(request, 'QR/QandA.html')  
     return render(request, 'QR/QandA.html')  

