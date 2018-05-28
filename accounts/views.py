from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Profile
from .forms import LoginForm

def main(request):
    template = 'main.html'
    context = {}
    if request.user.is_authenticated:
        user_data = Profile.objects.get(email=request.user)
        context['email'] = user_data.email
        # context[]
        if user_data.photo:
            context['photo'] = user_data.photo
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
