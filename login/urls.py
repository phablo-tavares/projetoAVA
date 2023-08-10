from django.urls import include, path
from login.views import login_page, Autenticar, Logout_user
urlpatterns = [
    path('',  login_page),
    path('dologin', Autenticar),
    path('dologout', Logout_user, name='Logout')

]
