from django.core.mail import send_mail ,EmailMessage
from django.conf import settings
from django.shortcuts import redirect

def send_email_to_client(request):
    subject="from celestial coders"
    message="Hello , ki haal chaal sab thik??"
    from_email=settings.EMAIL_HOST_USER
    mail="ankitsingh160802@gmail.com"
    recipient_list=[mail]
    send_mail(subject,message,from_email,recipient_list)
    return redirect('Home')
def send_email_with_attachment(subject ,message,recipient_list,file_path):
    mail=EmailMessage(subject=subject,body=message,from_email=settings.EMAIL_HOST_USER ,to=recipient_list)
    mail.attach_file(file_path)
    mail.send()

