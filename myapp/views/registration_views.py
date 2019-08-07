from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import BadHeaderError, EmailMessage, send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

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
            user.save()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user.pk)
            email_context = {"token": token,
                             "uid": uid,
                             "domain": get_current_site(request).domain}
            mail = EmailMessage(
                "Inventarium: Confirmation de l'inscription",
                render_to_string("myapp/user/activate_account.html",
                    context=email_context),
                EMAIL_HOST_USER,
                [user.email]
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
                    request, "Vous êtes connecté {}".format(email))
                return redirect('homepage')
            else:
                messages.error(
                    request, "Email ou mot de passe invalide.",
                    "danger")
        else:
            messages.error(
                request, "Email ou mot de passe invalide.",
                "danger")

    form = AuthenticationForm()

    return render(request=request,
                  template_name="myapp/user/signin.html",
                  context={"form": form})


def signout(request):
    """User disconnection."""
    logout(request)
    messages.info(request, 'Vous êtes déconnecté avec succès...')
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
            messages.success(request, f'Votre compte a bien été mis à jour.')
            return redirect('account')
    else:
        u_form = CustomUserChangeForm(instance=request.user)

    return render(request, 'myapp/user/account_update.html',
                  {'u_form': u_form})


def change_password(request):
    from django.contrib.auth.forms import PasswordChangeForm
    from django.contrib.auth import update_session_auth_hash

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
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
    return render(request, 'myapp/pages/contact.html', {'form': form})


def email_success(request):
    """Contact form email success"""

    return render(request, 'myapp/pages/contact_success.html')
