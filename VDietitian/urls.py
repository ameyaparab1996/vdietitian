"""VDietitian URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from dietplan import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls, name='adminPage'),
    # url(r'^dietplan/$',include('dietplan.urls')),
    url(r'^user/login/$', views.user_login, name='signin'),
    url(r'^user/logout/$', views.user_logout, name='logout'),
    url(r'^user/register/$', views.user_register, name='register'),
    url(r'^user/(?P<pk>\d+)/profile/$', views.user_profile, name='profile'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^password_reset/$', auth_views.password_reset,
        {'template_name':'resetPassword/password_reset_form.html',
         'subject_template_name':'resetPassword/password_reset_subject.txt',
         'email_template_name':'resetPassword/password_reset_email.html'},
        name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, {'template_name':'resetPassword/password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,{'template_name':'resetPassword/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete,{'template_name':'resetPassword/password_reset_complete.html'}, name='password_reset_complete'),
    url(r'^user/(?P<pk>\d+)/form/$', views.UserInfoView, name='uif'),
    url(r'^user/feedback/$', views.feedbackView, name='feedback'),
    url(r'^user/feedbackSubmitted/$', views.feedbackView, name='feedback'),
]
