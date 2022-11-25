from django.shortcuts import render
from django import forms
# Create your views here.
# pages/views.py
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render
import qrcode
import qrcode.image.svg
from io import BytesIO
from django.core import mail
from django.core.mail import send_mail
from django.core import mail
import smtplib
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from email.message import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from .data import *
import html
from django.utils.html import escape

send_mail(
    subject = 'Test Mail',
    message = 'Maria V',
    from_email = 'maria.vasilache02@gmail.com',
    recipient_list = ['maria.vasilache02@gmail.com',],
    fail_silently = False,
)

class EmailForm(forms.Form):
     recipient = forms.EmailField()
     message = forms.CharField(widget=forms.Textarea)


class HomePageView(TemplateView):
    template_name = 'home.html'

def newCV(request):
      #se preiau toate datele din interfata si se vor pune in baza de date;



    return render(request, 'QR/newCV.html')  

# def myCv(request):
#      return render(request, 'QR/MyCV.html')  

def qr(request):
     return render(request, 'QR/QRcode.html')  

def qaa(request): 

# create a variable to keep track of the form
    messageSent = False
    recipient = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    server=smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login("maria.vasilache02@gmail.com", "qgrqmaoreadfcszp")

    # check if form has been submitted
    if request.method == 'POST':

        form = EmailForm(request.POST)

        # check if data from the form is clean
        if form.is_valid():
            cd = form.cleaned_data
            subject = "CV-issue"
            message = cd['message']
            emm=cd['recipient']
            files = request.FILES.getlist('attach')
            #attach = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
           # server.sendmail("maria.vasilache02@gmail.com", ["maria.vasilache02@gmail.com", [cd['recipient']]], subject+"\n"+message) 
           # server.quit()
            files
            email = EmailMessage()

            email['Subject'] = subject
            email['From'] = emm
            email['To'] = 'maria.vasilache02@gmail.com'
            email.set_content("S-a primit o solicitare de la "+emm+"\n\n"+ "Mesajul transmis:\n "+message+"\n"+"\nATENTIE: Este posibil sa fie incarcate atasamenta!!")

            with open('D:\An3\IS\P1\cv_Maria_Vasilache.pdf', 'rb') as content_file:
                
                content = content_file.read()
                email.add_attachment(content, maintype='application', subtype='pdf', filename='cv.pdf')

            server.send_message(email)
            

            messageSent = True

    else:
        form = EmailForm()

    return render(request, 'QR/QandA.html', {

        'form': form,
        'messageSent': messageSent,

    })


def qr(request):
     context = {}
     if request.method == "POST":
          factory = qrcode.image.svg.SvgImage
          img = qrcode.make(request.POST.get("qr_text",""), image_factory=factory, box_size=20)
          stream = BytesIO()
          img.save(stream)
          context["svg"] = stream.getvalue().decode()

     return render(request, "QR/QRcode.html", context=context)



def getSkills():
    i = 0
    gotoshow = ""
    while i < len(yourSkills):
        skill = "<li><span class='main full'>" + yourSkills[i] + "</span></li>"
        i += 1
        gotoshow = gotoshow + skill
        if i == len(yourSkills):
            return html.unescape(gotoshow)

def getList(shema):
    i = 0
    gotoshow = ""
    while i < len(shema):
        skill = "<li>" + shema[i] + "</li>"
        i += 1
        gotoshow = gotoshow + skill
        if i == len(shema):
            return html.unescape(gotoshow)

def getListWithYear(shema, year):
    i = 0
    gotoshow = ""
    while i < len(shema):
        if year[i]:
           skill = "<li><span class='main'>" + shema[i] + "</span><span class='year'>" + year[i] + "</span></li>"
        else:
           skill = "<li><span class='main full'>" + shema[i] + "</span></li>"
        i += 1
        gotoshow = gotoshow + skill
        if i == len(shema):
            return html.unescape(gotoshow)

def getListWithLink(shema, link):
    i = 0
    gotoshow = ""
    while i < len(shema):
        if link[i]:
            skill = "<li><a target='_blank' href='" + link[i] + "'>" + shema[i] + "</a></li>"
        else:
            skill = "<li><a target='_blank'>" + shema[i] + "</a></li>"
        i += 1
        gotoshow = gotoshow + skill
        if i == len(shema):
            return html.unescape(gotoshow)

def getSocials(shema, link):
    i = 0
    gotoshow = ""
    while i < len(shema):
        if link[i]:
            skill = "<a class='social' target='_blank' href='" + link[i] + "'><i class='" + shema[i] + "'></i></a>"
            gotoshow = gotoshow + skill
        else:
            gotoshow = gotoshow
        i += 1
        if i == len(shema):
            return html.unescape(gotoshow)

def data():
    #sa le preia din baza de date
    return {
        'titleCV' : titleCV,
        'yourName' : yourName,
        'yourProfession' : yourProfession,
        'yourBio' : yourBio,
        'yourCountry' : yourCountry,
        'yourContact' : getSocials(socialContact, yourContact),
        'yourBirthday' : yourBirthday,
        'yourSkills' : getSkills(),
        'yourHobbies' : getList(yourHobbies),
        'yourCerts' : getList(yourCerts),
        'yourEdu' : getListWithYear(yourEdu, eduYear),
        'yourWork' : getListWithYear(yourWork, workYear),
        'yourProject' : getListWithLink(yourProject, projectLink),
        'yourExtras': getList(yourExtras),
        'footerText': footerText
        }

def myCv(request):
     return render(request, 'QR/MyCV.html',  data())  
#def home(request):
    #return render(response, "templates/home.html")