from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,
                              redirect, render)
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from .forms import UserRegisterForm, UserUpdateForm, EquipmentForm, RoomForm

# from .models import Equipment, Room


def homepage(request):
    """Display homepage."""
    template_name = 'index.html'
    return render(request, template_name)


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
            return redirect(reverse('homepage'))
    else:
        form = UserRegisterForm()

    template_name = 'register.html'
    context = {
        'form': form,
        'title': "S'enregister"
    }
    return render(request, template_name, context)

@login_required
def register_update(request):
    """Update account."""
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            # message.success(request, f'Votre compte a bien été mis à jour')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
    
    template_name = 'update_register.html'
    return render(request, template_name, {'u_form': u_form})

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

@login_required
def profile(request):
    """Display the user profile page."""
    context = {'user': request.user}
    template_name = 'profile.html'
    return render(request, template_name, context)

@login_required
def dashboard(request):
    """Display the user account page."""
    context = {
        'equipment': EquipmentForm,
        'room': RoomForm
        }
    template_name = 'dashboard.html'
    return render(request, template_name, context)

@login_required
def equipment_add(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = EquipmentForm()
    return render(request, 'equipment_add.html', {
        'form': form
    })

@login_required
def room_add(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = RoomForm()
    return render(request, 'room_add.html', {
        'form': form
    })

