from datetime import timedelta

from django.test import TestCase, Client
from django.utils import timezone

from security.models import CustomUser

# Create your tests here.
class LoginTestCase(TestCase):
    def test_good_request(self):
        user = CustomUser(email="good@example.com")
        user.save()
        
        # check that we can get the page
        client = Client()
        response = client.get("/security/send_login_token/")
        assert response.content.find("form") > -1
        
        # check that we can get the token
        response = client.post("/security/send_login_token/", 
                               {"email" : "good@example.com"}, follow=True)
        assert response.content.find("sent to your email") > 1
        
        c2 = CustomUser.objects.get(email="good@example.com")
        assert c2.login_token is not None
        assert timezone.now() + timedelta(hours=24) > c2.login_token_expires
        
        # check that we can login using that token and then it is destroyed
        response = client.get(
            "/security/login_with_token/{}/".format(c2.login_token),
            follow=True)
        assert response.content.find("Hello World!") > -1
        c3 = CustomUser.objects.get(email="good@example.com")
        assert c3.login_token is None
        
    def test_bogus_token(TestCase):
        client = Client()

        response = client.get("/security/login_with_token/123/", follow=True)
        assert response.content.find("Invalid or expired") > -1
        
    def test_expired_token(TestCase):
        user = CustomUser(email="expired@example.com")
        user.save()
        
        # check that we can get the page
        client = Client()
        response = client.get("/security/send_login_token/")
        assert response.content.find("form") > -1

        # set the token back
        c2 = CustomUser.objects.get(email="expired@example.com")
        c2.login_token_expires = timezone.now() + timedelta(hours=24)
        c2.save()
        
        response = client.get(
            "/security/login_with_token/{}/".format(c2.login_token),
            follow=True)        
        assert response.content.find("Invalid or expired") > -1