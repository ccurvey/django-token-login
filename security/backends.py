from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class TokenBackend(object):
    """ Authenticate user by username or email """
    def authenticate(self, login_token):
        try:
            user = UserModel.objects.get(login_token=login_token)
            if user.login_token_expires < timezone.now():
                messages.error(request, "the password key is expired")
                return None
            user.login_token = None
            user.login_token_expires = None
            user.save()
            return user
        except UserModel.DoesNotExist:
            return None
 
    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None