from django.shortcuts import render
from .models import Profile

def main(request):
    template = 'main.html'
    context = {}
    if request.user.is_authenticated:
        user_data = Profile.objects.get(email=request.user)
        context['email'] = user_data.email
        if user_data.photo:
            context['photo'] = user_data.photo
    return render(request, template, context)

def empty_view(request):
    template = 'empty.html'
    context = {}
    return render(request=request, template_name=template, context=context)

# Create your views here.
