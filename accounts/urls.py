from django.conf.urls import url, include
from . import views
from django.contrib.auth.views import logout
from registration.backends.simple.views import RegistrationView as _RegistrationView
from .forms import AccountRegistrationForm

class RegistrationView(_RegistrationView):
    def get_success_url(self, user):
        return '/login/'


urlpatterns = [
    url(r'^main$', views.main, name='main_page'),
    url('^not_exists/', views.empty_view, name='empty_page'),
    url('^login/', views.login_user, name='log-in'),
    url('^logout/', logout, {'template_name': 'empty.html', 'next_page': '/login'}, name='logout'),
    url(r'^accounts/register', RegistrationView.as_view(form_class=AccountRegistrationForm), name='registration.register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^main/edit_account', views.edit_account, name='edit_page')
]