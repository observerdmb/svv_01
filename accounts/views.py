from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Profile
from .forms import LoginForm, AccountEditForm
from django.core.files.storage import FileSystemStorage as _FileSystemStorage
import os
from datetime import datetime
from django.utils.functional import cached_property
from django.utils.datastructures import MultiValueDictKeyError

class FileSystemStorage(_FileSystemStorage):
    @cached_property
    def base_location(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        MEDIA_ROOT = os.path.join(BASE_DIR, 'img')
        path_suffix ='profiles'
        path_year = datetime.today().strftime('%Y')
        path_month = datetime.today().strftime('%m')
        path_day = datetime.today().strftime('%d')
        filepath = os.path.join(MEDIA_ROOT, path_suffix, path_year, path_month, path_day)
        print(filepath)
        return self._value_or_setting(self._location, filepath)

class NoPhoto():
    url = '/media/profiles/unknown.png'


def main(request):
    template = 'main.html'
    context = {}
    if request.user.is_authenticated:
        user_data = Profile.objects.get(email=request.user)
        context['email'] = user_data.email
        context['nick'] = user_data.nick_name
        context['full_name'] = user_data.full_name
        context['country'] = user_data.country
        context['city'] = user_data.city
        context['birth'] = user_data.date_of_birth
        context['about_me'] = user_data.about_me
        if user_data.photo:
            context['photo'] = user_data.photo
        else:
            no_photo = NoPhoto()
            context['photo'] = no_photo
    return render(request, template, context)

def edit_account(request):
    user_data = Profile.objects.get(email=request.user)
    if request.method == 'POST':
        form = AccountEditForm(request.POST, request.FILES)
        if form.is_valid():
            edited_details = form.cleaned_data
            if edited_details['full_name']:
                user_data.full_name = edited_details['full_name']
            if edited_details['nick_name']:
                user_data.nick_name = edited_details['nick_name']
            if edited_details['date_of_birth']:
                user_data.date_of_birth = edited_details['date_of_birth']
            if edited_details['about_me']:
                user_data.about_me = edited_details['about_me']
            if edited_details['city']:
                user_data.city = edited_details['city']
            if edited_details['country']:
                user_data.country = edited_details['country']
            try:
                if edited_details['photo']:
                    avatar = edited_details['photo']
                    fs = FileSystemStorage()
                    filename = fs.save(avatar.name, avatar)
                    filepath = os.path.join(fs.location, filename)
                    user_data.photo = filepath
            except MultiValueDictKeyError:
                pass
            user_data.save()
        return redirect(main)
    template = 'edit_account.html'
    form = AccountEditForm()
    if user_data.full_name:
        form.fields['full_name'].widget.attrs['placeholder'] = user_data.full_name
    if user_data.nick_name:
        form.fields['nick_name'].widget.attrs['placeholder'] = user_data.nick_name
    if user_data.date_of_birth:
        form.fields['date_of_birth'].widget.attrs['placeholder'] = user_data.date_of_birth.strftime('%d.%m.%Y')
    if user_data.about_me:
        form.fields['about_me'].widget.attrs['placeholder'] = user_data.about_me
    if user_data.city:
        form.fields['city'].widget.attrs['placeholder'] = user_data.city
    if user_data.country:
        form.fields['country'].widget.attrs['placeholder'] = user_data.country
    context = {'edit_account_form': form}
    return render(request, template, context)


def search(request):
    template = 'search.html'
    context = {}
    if request.method == 'POST':
        query = request.POST['query']
        result = Profile.objects.filter(nick_name=query)
        context['results'] = result
    return render(request, template, context)


def login_user(request):
    template = 'login.html'
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            username = form_data['email'].lower()
            password = form_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(main)
            else:
                invalid_login = True
                return render(request, template, {'login_form': form, 'invalid_login': invalid_login})
        print(form)
    form = LoginForm()
    return render(request, template, {'login_form': form})

def empty_view(request):
    template = 'empty.html'
    context = {}
    return render(request=request, template_name=template, context=context)

# Create your views here.
