from django.conf.urls import url, include
from . import views
from django.contrib.auth.views import logout
from registration.backends.simple.views import RegistrationView as _RegistrationView
from .forms import AccountRegistrationForm
from django.views.generic import RedirectView

class RegistrationView(_RegistrationView):
    def get_success_url(self, user):
        return '/main/'


urlpatterns = [
    url(r'main/$', views.main, name='main_page'),
    url(r'^not_exists/', views.empty_view, name='empty_page'),
    url(r'^login/', views.login_user, name='log-in'),
    url(r'^logout/', logout, {'template_name': 'empty.html', 'next_page': '/main'}, name='logout'),
    url(r'^accounts/register', RegistrationView.as_view(form_class=AccountRegistrationForm), name='registration.register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^main/edit_account', views.edit_account, name='edit_page'),
    url(r'^$', RedirectView.as_view(pattern_name='main_page'))
]