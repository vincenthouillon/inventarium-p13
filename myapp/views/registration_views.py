from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import BadHeaderError, send_mail
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse

from ..forms import ContactForm, UserSignupForm, UserUpdateForm
from inventarium.settings import EMAIL_HOST_USER


def index(request):
    """View the home page."""
    template_name = 'myapp/index.html'
    return render(request, template_name)


def about(request):
    """Display about page."""
    template_name = 'myapp/about.html'
    return render(request, template_name)


def signup(request):
    """User registration page."""
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse('homepage'))
    else:
        form = UserSignupForm()

    template_name = 'myapp/signup.html'
    context = {
        'form': form,
        'title': "S'enregister"
    }
    return render(request, template_name, context)


def terms(request):
    """Display about page."""
    template_name = 'myapp/terms.html'
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
                  template_name="myapp/signin.html",
                  context={"form": form})


def signout(request):
    """User disconnection."""
    logout(request)
    messages.info(request, 'Vous êtes déconnecté avec succès...')
    return redirect('index')


@login_required
def account(request):
    """Display the user profile page."""
    return render(request, 'myapp/account.html', {'user': request.user})


@login_required
def account_update(request):
    """Update account."""
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Votre compte a bien été mis à jour.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    return render(request, 'myapp/account_update.html', {'u_form': u_form})


@login_required
def user_delete(request):
    """Delete user in database."""
    user = request.user
    user.delete()
    logout(request)
    messages.success(request, 'Votre compte est supprimé.')
    return redirect('index')


def email(request):
    """Contact form."""
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = """Expediteur : {}\n Sujet : {}\n Message : {}\n"""\
                .format(form.cleaned_data['from_email'],
                        form.cleaned_data['subject'],
                        form.cleaned_data['message'])
            try:
                send_mail(subject, message, from_email, [EMAIL_HOST_USER])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('email_success')
    return render(request, 'myapp/contact.html', {'form': form})


def email_success(request):
    """Contact form email success"""

    return render(request, 'myapp/contact_success.html')
