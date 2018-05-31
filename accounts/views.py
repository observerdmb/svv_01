from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Profile
from .forms import LoginForm, AccountEditForm


class NoPhoto():
    url = 'media\\profiles\\unknown.png'


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
        edited_details = request.POST
        if edited_details['full_name'] is not '':
            user_data.full_name = edited_details['full_name']
        if edited_details['nick_name'] is not '':
            user_data.nick_name = edited_details['nick_name']
        if edited_details['date_of_birth'] is not '':
            user_data.date_of_birth = edited_details['date_of_birth']
        if edited_details['about_me'] is not '':
            user_data.about_me = edited_details['about_me']
        if edited_details['city'] is not '':
            user_data.city = edited_details['city']
        if edited_details['country'] is not '':
            user_data.country = edited_details['country']
        user_data.save()

    template = 'edit_account.html'
    form = AccountEditForm()
    form.fields['full_name'].widget.attrs['placeholder'] = user_data.full_name
    form.fields['nick_name'].widget.attrs['placeholder'] = user_data.nick_name
    form.fields['date_of_birth'].widget.attrs['placeholder'] = user_data.date_of_birth
    form.fields['about_me'].widget.attrs['placeholder'] = user_data.about_me
    form.fields['city'].widget.attrs['placeholder'] = user_data.city
    form.fields['country'].widget.attrs['placeholder'] = user_data.country


    context = {'edit_account_form': form}
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
        print(form)
    form = LoginForm()
    return render(request, template, {'login_form': form})

def empty_view(request):
    template = 'empty.html'
    context = {}
    return render(request=request, template_name=template, context=context)

# Create your views here.
