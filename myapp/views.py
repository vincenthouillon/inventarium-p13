from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,
                              redirect, render)
from django.urls import reverse

from .forms import SignupForm


def homepage(request):
    """Display homepage."""
    template_name = 'index.html'
    return render(request, template_name)

def about(request):
    """Display about page."""
    template_name = 'about.html'
    return render(request, template_name)


def signup(request):
    """User registration page."""
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse('homepage'))
    else:
        form = SignupForm()

    template_name = 'signup.html'
    context = {
        'form': form,
        'title': "S'enregister"
    }
    return render(request, template_name, context)


def signin(request):
    """User login page."""
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(
                    request, "Vous êtes connecté {}".format(username))
                return redirect('/')
            else:
                messages.error(
                    request, "Nom d'utilisateur ou mot de passe invalide.")
        else:
            messages.error(
                request, "Nom d'utilisateur ou mot de passe invalide.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="signin.html",
                  context={"form": form})


def signout(request):
    """User disconnection."""
    logout(request)
    messages.add_message(request, messages.INFO,
                         'Vous êtes déconnecté avec succès...')
    return redirect('homepage')
