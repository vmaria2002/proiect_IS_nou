from django.shortcuts import render
import io
import html
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.core.mail import EmailMessage
from email.message import EmailMessage
# Create your views here.
# pages/views.py
from django.utils.html import escape
from django import forms
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render
import qrcode
import qrcode.image.svg
import smtplib
import requests
from io import BytesIO
from django.http import StreamingHttpResponse
from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server
import mimetypes
import os
from wsgiref.util import FileWrapper
from fpdf import FPDF
import codecs
from pages.data import *
# pt pdf
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

class EmailForm(forms.Form):
     recipient = forms.EmailField()
     message = forms.CharField(widget=forms.Textarea)

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
def getLists(shema):
    i = 0
    gotoshow = ""
    while i < len(shema):
        skill = "<li>" + shema[i] + "</li>"
        i += 1
        gotoshow = gotoshow + skill
        if i == len(shema):
            return html.unescape(gotoshow)
def getSocial(shema, link):
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
def getListWithYea(shema, year):
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
def getListWithLin(shema, link):
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

val= {
        'titleCV' : titleCV,
        'yourName' : yourName,
        'yourProfession' : yourProfession,
        'yourBio' : yourBio,
        'yourCountry' : yourCountry,
         'yourContact' : getSocial(socialContact, yourContact),
        'yourBirthday' : yourBirthday,
         'yourHobbies' : getLists(yourHobbies),
         'yourCerts' : getLists(yourCerts),
         'yourEdu' : getListWithYea(yourEdu, eduYear),
         'yourWork' : getListWithYea(yourWork, workYear),
         'yourProject' : getListWithLin(yourProject, projectLink),
         'yourExtras': getLists(yourExtras),
        'footerText': footerText
        }

def data():
    #sa le preia din baza de date
    val['yourName']="Ana"
    rez= {
        'titleCV' : titleCV,
        'yourName' : yourName,
        'yourProfession' : yourProfession,
        'yourBio' : yourBio,
        'yourCountry' : yourCountry,
         'yourContact' : getSocial(socialContact, yourContact),
        'yourBirthday' : yourBirthday,
         'yourHobbies' : getLists(yourHobbies),
         'yourCerts' : getLists(yourCerts),
         'yourEdu' : getListWithYea(yourEdu, eduYear),
         'yourWork' : getListWithYea(yourWork, workYear),
         'yourProject' : getListWithLin(yourProject, projectLink),
         'yourExtras': getLists(yourExtras),
        'footerText': footerText
        }
    return rez

def qaa(request):
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

            with open('D:\An3\IS\Download\cv.mhtml', 'rb') as content_file:
                
                content = content_file.read()
                email.add_attachment(content, maintype='application', subtype='mhtml', filename='cv.pdf')

            server.send_message(email)
            

            messageSent = True

    else:
        form = EmailForm()





def downloadFile(request):   

     base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
     filename='CV.mhtml'
     thefile= base_dir + '/Files/'+ filename
     filename = os.path.basename(thefile)
     chunk_size =8192
     reponse = StreamingHttpResponse(FileWrapper(open(thefile, 'rb'), chunk_size), content_type =mimetypes.guess_type(thefile)[0])
     reponse['Content-Length']=os.path.getsize(thefile)
     reponse['Content-Disposition']="Attachment;filename=%s" % filename
     return reponse

#pentru pagina cv
# def index(request):
#    if request.method == 'POST':
#       user = request.POST['user']
#       passu = request.POST['pass']

#functie pentru detectarea tarii:
def country(nr):
    rez=""
    if nr=="1":
        rez="Romania/Cluj-Napoca"
    elif nr=="2":
        rez="Romania/Iasi"
    else:
        rez="France/Paris"

    return rez

socialContact = [
        'fab fa-github',
        'fab fa-linkedin',
        'fab fa-facebook',
    ]

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

def getSkills(yourSkills):
    rez=yourSkills.split(", ")
    i = 0
    gotoshow = ""
    while i < len(rez):
        skill = "<li><span class='main full'>" + rez[i] + "</span></li>"
        i += 1
        gotoshow = gotoshow + skill
        if i == len(rez):
            return html.unescape(gotoshow)


def getListWithYear(shema, year):
    i = 0
    gotoshow = ""
    skill = "<li><span class='main'>" + shema + "</span><span class='year'>" + year + "</span></li>"
    gotoshow = gotoshow + skill

    return html.unescape(gotoshow)

def getListWithLink(shema, link):
    i = 0
    gotoshow = ""
    skill = "<li><a target='_blank' href='" + link + "'>" + shema + "</a></li>"
    gotoshow = gotoshow + skill
    return html.unescape(gotoshow)


def index(request):
      return render(request, 'index.html')
def validate(request):
   if request.method == 'POST':
      prenume= request.POST['prenume']
      nume=request.POST['nume']
      attach= "/static/img/"+request.POST['attach']
      
      profession=request.POST['profession']
      yourBio=request.POST['yourBio']
      yourCountry=country(request.POST['yourCountry'])

      yourBirthday=request.POST['yourBirthday']


      git=request.POST['gitHub']
      linkedin= request.POST['linkedin']      
      facebook=request.POST['facebook']  
      yourContac = [git, linkedin, facebook]
    

      yourContact = getSocials(socialContact, yourContac)

      yourSkill =request.POST['yourSkills']  
      yourSkills =getSkills(yourSkill)

      yourHobbie =request.POST['yourHobbies']  
      yourHobbie =getSkills(yourHobbie)

      eduYear=request.POST['eduYear']  
      yourEdus=request.POST['yourEdu']   
      yourEdu = getListWithYear(yourEdus, eduYear)

      work=request.POST['work']  
      year_work=request.POST['year_work']  

      yourWork=getListWithYear(work, year_work)

      yourProjects=request.POST['yourProject']
      projectLink=request.POST['projectLink']  
       
      yourProject=getListWithLink(yourProjects, projectLink)

      val['yourName']=prenume+" "+nume
      val['profession']=profession
      val['yourBio']=yourBio
      val['attach']=attach
      val['yourCountry']=yourCountry
      val['yourBirthday']=yourBirthday 
      val['socialContact']=socialContact
      val['yourContact']= yourContact
      val['yourSkills']=yourSkills
      val['yourHobbies']=yourHobbie
      val['yourEdu']=yourEdu
      val['yourWork']=yourWork
      val['yourProject']=yourProject  

      dict = {
         'prenume': prenume+" "+nume,
         'profession':profession,
          'yourBio':yourBio,
          'attach':attach,
          'yourCountry':yourCountry,
          'yourBirthday':yourBirthday,
          'socialContact':socialContact,
          'yourContact': yourContact,
          'yourSkills':yourSkills,
          'yourHobbies':yourHobbie,
          'yourEdu':yourEdu,
           'yourWork':yourWork,
           'yourProject' :yourProject

        #  'password': password,
        
      }
     
      return render(request, 'validate.html', dict)   



def pdf_report_create(request):

    dict = val
       
    template_path = 'pdfReport.html'

    context =dict

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="cv_report.pdf"'

    template = get_template(template_path)

    html = template.render(context)

# create a pdf
    pisa_status = pisa.CreatePDF(  html, dest=response)
# if error then show some funy view
    if pisa_status.err:
     return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response 