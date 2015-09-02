import hashlib
import time
from datetime import timedelta
from django.shortcuts import render, redirect
from django import forms
from django.core.mail import send_mail
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib import messages
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.conf import settings

UserModel = get_user_model()

# Create your views here.

class LoginTokenRequestForm(forms.Form):
    email = forms.EmailField()

LOGIN_MESSAGE = """
Please use this link to login to our system:

{}
"""    
def send_login_token(request):
    if request.method == 'POST':
        form = LoginTokenRequestForm(request.POST)
        if form.is_valid():
            try:
                user = UserModel.objects.get(email=form.cleaned_data['email'])
            except UserModel.DoesNotExists:
                messages.warn(request, "No such user")
                return redirect(reverse("security.views.send_login_token"))
            
            m = hashlib.md5()
            m.update(time.asctime())
            user.login_token = m.hexdigest()
            user.login_token_expires = timezone.now() + timedelta(hours=24)
            user.save()
            
            link = request.build_absolute_uri(
                reverse('security.views.login_with_token', 
                        kwargs={"login_token" : user.login_token}))
            
            send_mail(subject="login token", 
                      message=LOGIN_MESSAGE.format(link),
                      from_email="noreply", recipient_list=[user.email,])
            
            messages.success(request, "login token sent to your email")
            return redirect("/")
    else:
        form = LoginTokenRequestForm()

    return render(request, "send_login_token.html", {"form" : form})

def login_with_token(request, login_token):
    import wingdbstub
    user = authenticate(login_token=login_token)
    if user and user.is_active:
        login(request, user)
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        messages.error(request, "Invalid or expired token.  Try again?")
        return redirect(reverse("security.views.send_login_token"))
    
def hello(request):
    return render(request, "hello.html")