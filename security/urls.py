from django.conf.urls import url, patterns

urlpatterns = patterns("security.views",
    url("send_login_token/", 'send_login_token'), 
    url("login_with_token/(?P<login_token>.*)/$", "login_with_token"), 
    url("hello/", "hello"), 
)