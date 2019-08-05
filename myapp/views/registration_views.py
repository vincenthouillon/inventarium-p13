from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.urls import reverse

from ..forms import (UserRegisterForm, UserUpdateForm)


def index(request):
    """View the home page with the user's login form."""
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
                return redirect('homepage')
            else:
                messages.error(
                    request, "Nom d'utilisateur ou mot de passe invalide.",
                    "danger")
        else:
            messages.error(
                request, "Nom d'utilisateur ou mot de passe invalide.",
                "danger")

    form = AuthenticationForm()

    template_name = 'index.html'
    return render(request, template_name, {'form': form})


def about(request):
    """Display about page."""
    template_name = 'about.html'
    return render(request, template_name)


def register(request):
    """User registration page."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse('index'))
    else:
        form = UserRegisterForm()

    template_name = 'register.html'
    context = {
        'form': form,
        'title': "S'enregister"
    }
    return render(request, template_name, context)


def terms(request):
    """Display about page."""
    template_name = 'terms.html'
    return render(request, template_name)


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
                return redirect('homepage')
            else:
                messages.error(
                    request, "Nom d'utilisateur ou mot de passe invalide.",
                    "danger")
        else:
            messages.error(
                request, "Nom d'utilisateur ou mot de passe invalide.",
                "danger")

    form = AuthenticationForm()

    return render(request=request,
                  template_name="signin.html",
                  context={"form": form})


def signout(request):
    """User disconnection."""
    logout(request)
    messages.info(request, 'Vous êtes déconnecté avec succès...')
    return redirect('index')


@login_required
def profile(request):
    """Display the user profile page."""
    return render(request, 'profile.html', {'user': request.user})


@login_required
def profile_update(request):
    """Update account."""
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Votre compte a bien été mis à jour.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    return render(request, 'profile_update.html', {'u_form': u_form})


@login_required
def user_delete(request):
    """Delete user in database."""
    user = request.user
    user.delete()
    logout(request)
    messages.success(request, 'Votre compte est supprimé.')
    return redirect('index')
