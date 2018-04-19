from django.conf.urls import url

from django_cognito import views


urlpatterns = [
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^login_callback/', views.login_callback, name='login_callback'),
    url(r'^logout_callback/', views.logout_callback, name='logout_callback'),
]


