from django.conf.urls import url
from . import views
from django.contrib.auth.views import logout


urlpatterns = [
    url(r'^main', views.main, name='main_page'),
    url('^not_exists/', views.empty_view, name='empty_page'),
    url('^login/', views.login_user, name='log-in'),
    url('^logout/', logout, {'template_name': 'empty.html', 'next_page': '/login'}, name='logout'),
]