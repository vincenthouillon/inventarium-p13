from django.contrib import messages
from django.contrib.auth import (authenticate, get_user_model, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import BadHeaderError, EmailMessage, send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from sentry_sdk import capture_message

from inventarium.settings import EMAIL_HOST_USER

from ..forms import ContactForm, CustomUserChangeForm, CustomUserCreationForm
from ..tokens import account_activation_token


def index(request):
    """View the home page."""
    template_name = 'myapp/pages/index.html'
    return render(request, template_name)


def about(request):
    """Display about page."""
    template_name = 'myapp/pages/about.html'
    return render(request, template_name)


def signup(request):
    """User registration with confirmation email."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            capture_message(user.email, level='info')  # sentry log
            user.save()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user.pk)
            email_context = {"token": token,
                             "uid": uid,
                             "domain": get_current_site(request).domain}
            mail = EmailMessage(
                subject="Inventarium: Confirmation de l'inscription",
                body=render_to_string("myapp/user/activate_account.html",
                                         context=email_context),            
                from_email='admin@inventarium.me',
                to=[user.email]
            )
            mail.content_subtype = "html"
            mail.send()
            return render(request, "myapp/user/signup_email.html")
    else:
        form = CustomUserCreationForm()

    template_name = 'myapp/user/signup.html'
    context = {
        'form': form,
        'title': "S'enregister"
    }

    return render(request, template_name, context)


def activate_account(request, uid, token):
    """Manage view for link account activation."""
    User = get_user_model()

    try:
        user_id = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        context = {"is_valid_data": False}
    else:
        if account_activation_token.check_token(user.id, token):
            user.is_active = True
            user.save()
            login(request, user)
            context = {"is_valid_data": True}
        else:
            context = {"is_valid_data": False}
    return render(request, "myapp/user/signup_validation.html", context)


def terms(request):
    """Display about page."""
    template_name = 'myapp/pages/terms.html'
    return render(request, template_name)


def signin(request):
    """User login page."""
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request,
                      user,
                      backend='django.contrib.auth.backends.ModelBackend')
                messages.info(
                    request, 'Vous êtes connecté {}'.format(email))
                return redirect('homepage')
            else:
                messages.error(
                    request, 'Email ou mot de passe invalide.',
                    'danger')
        else:
            messages.error(
                request, 'Email ou mot de passe invalide.',
                'danger')

    form = AuthenticationForm()

    capture_message(EMAIL_HOST_USER, level='info')  # sentry log
    return render(request=request,
                  template_name="myapp/user/signin.html",
                  context={"form": form})


def signout(request):
    """User disconnection."""
    logout(request)
    messages.info(request, 'Vous êtes déconnecté avec succès...', 'success')
    return redirect('index')


@login_required
def account(request):
    """Display the user account page."""
    return render(request, 'myapp/user/account.html', {'user': request.user})


@login_required
def account_update(request):
    """Update account."""
    if request.method == "POST":
        u_form = CustomUserChangeForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Votre compte a bien été mis à jour.',
                             'success')
            return redirect('account')
    else:
        u_form = CustomUserChangeForm(instance=request.user)

    return render(request, 'myapp/user/account_update.html',
                  {'u_form': u_form})


@login_required
def change_password(request):
    """Change password view."""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Votre mot de passe a bien été mis à jour', 'success')
            return redirect('account')
        else:
            messages.error(request, 'Veuillez corriger l\'erreur ci-dessous.',
                           'danger')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'myapp/user/change_password.html', {
        'form': form
    })


@login_required
def user_delete(request):
    """Delete user in database."""
    user = request.user
    user.delete()
    logout(request)
    messages.success(request, 'Votre compte est supprimé.', 'success')
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
    return render(request, 'myapp/pages/contact.html', {'form': form})


def email_success(request):
    """Contact form email success"""

    return render(request, 'myapp/pages/contact_success.html')
