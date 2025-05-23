#views of scan upload app

from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate ,login,logout,get_user_model
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
from . import Resumechecking

from .utils import send_email_with_attachment,send_email_to_client

from .tokens import account_activation_token

from io import StringIO

# for account activation


from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.core.mail import EmailMessage


# Create your views here.




def activate(request,uidb64,token):
    User=get_user_model()
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except:
        user=None
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,"email confirmed")
        return redirect('Home')
    else:
        messages.error(request,"invalid")
    return redirect('Home')

    return redirect('Home')


def activateEmail(request,user,to_email):
    mail_subject="activate your account"
    message=render_to_string('template_activate_account.html',{'user':to_email,'domain':get_current_site(request).domain,'uid':urlsafe_base64_encode(force_bytes(user.pk)),'token':account_activation_token.make_token(user),'protocol':'https' if request.is_secure() else 'http'})
    email=EmailMessage(mail_subject,message,to=[to_email])
    if email.send():

        messages.success(request,"please visit your email id for confirmation mail")
    else:
        messages.error(request,'check again')


def index(request):
    return HttpResponse("bye")
    #return render(request,'index.html')






def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        usercheck=User.objects.filter(username=username)
        if not usercheck.exists():
            messages.success(request,("username not found "))
            return redirect('login')
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return redirect('/?example_param=' + username)
            else:
                messages.success(request,("kindly enter the right password"))
                return redirect('login')
                # Return an 'invalid login' error message.
    else:
        return render(request,'login.html',{})


def logout_user(request):
    logout(request)
    messages.success(request,("logout successfully"))
    return redirect('Home')

def register_user(request):
    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password=request.POST.get('password')

        #checking for already taken usename
        user=User.objects.filter(username=username)

        if user.exists():
            messages.success(request,("usename already taken"))
            return redirect('register')

        user =User.objects.create(first_name=first_name,last_name=last_name,username=username)
        user.set_password(password)
        user.is_active=False
        user.save()
        activateEmail(request,user,username)

        login(request,user)

        return redirect('Home')

    else:
        return render(request,"register.html",{})



def validCandidate(result):
    result=result.lower()
    if "yes" in result:
        return True



# from django.core.files.storage import default_storage
list=[]
def resumechecker(request):
    if request.method == "POST":
        # list=[]
        job_desc=request.POST.get('job')
        Resumefile = request.FILES.getlist('resume')
        option=request.POST.get('shortlisting')
        print(option)
        for file in Resumefile:
            # You can handle each file here
            # Save file to the default storage
            # file_path = default_storage.save(file.name, file)
            result=Resumechecking.checking(file,job_desc,option)
            if option=="emails":
                if result!="none":
                    list.append(result)
            else:
                if (validCandidate(result)):
                    list.append(file)
            
        result=create_and_download_file(list)
        return render(request,"resumecheck.html",{'message':result})
    else:
        return render(request,'resumecheck.html',{})


def create_and_download_file(request):
    # Create a file-like buffer to receive the data
    buffer = StringIO()
    
    # Write some content to the buffer
    for item in list:
        buffer.write(str(item))
        buffer.write("\n")
    
    # Ensure the buffer's pointer is at the beginning
    buffer.seek(0)
    
    # Create the response
    response = HttpResponse(buffer, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="shortListed.txt"'
    
    return response