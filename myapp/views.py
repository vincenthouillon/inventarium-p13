from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django_tables2 import RequestConfig
from django_tables2.export.export import TableExport

from .forms import (EquipmentForm, ResidenceForm, RoomForm, UserRegisterForm,
                    UserUpdateForm)
from .models import Equipment, Residence, Room
from .tables import EquipmentTable


# region: Homepage and registration
def homepage(request):
    """Display homepage."""
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
                return redirect('dashboard')
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
            return redirect(reverse('homepage'))
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
                return redirect('dashboard')
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
    return redirect('homepage')


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
            messages.success(request, f'Votre compte a bien été mis à jour')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    return render(request, 'profile_update.html', {'u_form': u_form})


@login_required
def user_delete(request):
    user = request.user
    user.delete()
    logout(request)
    messages.success(request, 'Votre compte est supprimé')
    return redirect('homepage')
# endregion

# region: display pages
@login_required
def dashboard(request):
    """Display the user account page."""
    qs_residences = Residence.objects.filter(
        user=request.user).order_by('name')

    return render(request, 'dashboard.html', {'residences': qs_residences, })


@login_required
def residence(request, residence_id):
    """Display the rooms."""
    get_residence = get_object_or_404(
        Residence, id=residence_id, user=request.user)
    rooms = Room.objects.filter(residence=get_residence).order_by('name')

    return render(request, 'residence.html', {
        'rooms': rooms,
        'residence': get_residence,
    })


@login_required
def room(request, room_id):
    """Display the equipements in room."""
    get_room = get_object_or_404(Room, id=room_id)

    if get_room.residence in Residence.objects.filter(user=request.user):
        equipments = Equipment.objects.filter(room=get_room).order_by('name')
    else:
        raise Http404()

    return render(request, 'room.html', {
        'room': get_room,
        'equipments': equipments,
    })


@login_required
def room_equipment(request, room_id, record):
    """
    When you click on a line in the equipment table,
    displays the details of a device.
    """
    get_equipment = get_object_or_404(Equipment, id=record)

    if get_equipment.room.residence in Residence.objects.filter(
            user=request.user):
        equipments = get_object_or_404(Equipment, id=get_equipment.id)
    else:
        raise Http404()

    return render(request, 'equipment.html', {
        'equipment': equipments,
    })


@login_required
def room_list(request, room_id):
    """Displays an array of devices and add export in .xls."""
    get_room = get_object_or_404(Room, id=room_id)

    if get_room.residence in Residence.objects.filter(user=request.user):
        equipments = EquipmentTable(Equipment.objects.filter(room=get_room))

        RequestConfig(request).configure(equipments)

        export_format = request.GET.get('_export', None)
        if TableExport.is_valid_format(export_format):
            exporter = TableExport(export_format, equipments)
            return exporter.response('equipments.{}'.format(export_format))
    else:
        raise Http404()

    return render(request, 'room_list.html', {
        'room': get_room,
        'equipments': equipments,
    })


@login_required
def equipment(request, equipment_id):
    """Display the equipments in room."""
    get_equipment = get_object_or_404(Equipment, id=equipment_id)

    if get_equipment.room.residence in Residence.objects.filter(
            user=request.user):
        equipments = get_object_or_404(Equipment, id=get_equipment.id)
    else:
        raise Http404()

    return render(request, 'equipment.html', {
        'equipment': equipments,
    })
# endregion


# region: forms
@login_required
def residence_add(request):
    if request.method == 'POST':
        form = ResidenceForm(request.POST)
        if form.is_valid():
            home = form.save(commit=False)
            home.user = request.user  # The logged user
            home.save()
            return redirect('dashboard')
    else:
        form = ResidenceForm()
    return render(request, 'residence_add.html', {
        'form': form,
        'user': request.user
    })


@login_required
def residence_update(request, residence_id):
    """Update residence."""
    get_residence = get_object_or_404(
        Residence, pk=residence_id, user=request.user)

    if request.method == "POST":
        u_form = ResidenceForm(request.POST, instance=get_residence)
        if u_form.is_valid():
            u_form.save()
            messages.success(
                request, f'Votre résidence a bien été mise à jour')
            return redirect('dashboard')
    else:
        u_form = ResidenceForm(instance=get_residence)

    return render(request, 'residence_update.html', {'u_form': u_form})


def residence_delete(request, residence_id):
    if request.method == 'POST':
        residence = get_object_or_404(
            Residence, pk=residence_id, user=request.user)
        residence.delete()
    return redirect('dashboard')


@login_required
def room_add(request, residence_id):
    """Showing the add residence form."""
    get_residence = get_object_or_404(
        Residence, id=residence_id, user=request.user)

    if request.method == 'POST':
        u_form = RoomForm(request.POST, request.FILES)
        if u_form.is_valid():
            form = u_form.save(commit=False)
            form.residence = get_residence
            form.save()
            return redirect('residence', residence_id=get_residence.id)
        else:
            u_form = RoomForm()

    return render(request, 'room_add.html', {
        'form': RoomForm,
        'residence': get_residence
    })


@login_required
def room_update(request, room_id):
    """Showing the update residence form."""
    get_room = get_object_or_404(Room, id=room_id)

    # If the residence belongs to the residences of the user
    if get_room.residence in Residence.objects.filter(user=request.user):
        if request.method == 'POST':
            u_form = RoomForm(request.POST, request.FILES, instance=get_room)
            if u_form.is_valid():
                form = u_form.save(commit=False)
                form.residence = get_room.residence
                form.save()
                messages.success(
                    request, f'Votre pièce a bien été mise à jour')
                return redirect('residence',
                                residence_id=get_room.residence.id)
        else:
            u_form = RoomForm(instance=get_room)

        return render(request, 'room_update.html', {
            'form': u_form,
            'residence': get_room.residence
        })
    else:
        raise Http404()


def room_delete(request, room_id):
    get_room = get_object_or_404(Room, id=room_id)

    # If the residence belongs to the residences of the user
    if get_room.residence in Residence.objects.filter(user=request.user):
        if request.method == 'POST':
            room = Room.objects.get(id=get_room.id)
            room.delete()
    return redirect('residence', residence_id=get_room.residence.id)


@login_required
def equipment_add(request, room_id):
    """Showing the add residence form."""
    get_room = get_object_or_404(Room, pk=room_id)

    # If the residence belongs to the residences of the user
    if get_room.residence in Residence.objects.filter(user=request.user):
        if request.method == 'POST':
            u_form = EquipmentForm(request.POST, request.FILES)
            if u_form.is_valid():
                form = u_form.save(commit=False)
                form.room = get_room
                form.save()
                return redirect('room', room_id=get_room.id)
            else:
                u_form = EquipmentForm()

        return render(request, 'equipment_add.html', {
            'form': EquipmentForm,
            'room_id': get_room,
        })

    else:
        raise Http404()


@login_required
def equipment_update(request, equipment_id):
    """Showing the add residence form."""
    get_equipment = get_object_or_404(Equipment, id=equipment_id)

    # If the residence belongs to the residences of the user
    if get_equipment.room.residence in Residence.objects.filter(
            user=request.user):
        if request.method == 'POST':
            u_form = EquipmentForm(request.POST, request.FILES,
                                   instance=get_equipment)
            if u_form.is_valid():
                form = u_form.save(commit=False)
                form.room = get_equipment.room
                messages.info(
                    request,
                    'L\'équipement "{}" a bien été mis à jour.'.format(
                        form.name))
                form.save()
                return redirect('room', room_id=get_equipment.room.id)
        else:
            u_form = EquipmentForm(instance=get_equipment)

        return render(request, 'equipment_update.html', {
            'form': u_form,
            'equipment': get_equipment,
        })

    else:
        raise Http404()


def equipment_delete(request, equipment_id):
    get_equipment = get_object_or_404(Equipment, id=equipment_id)

    # If the residence belongs to the residences of the user
    if get_equipment.room.residence in Residence.objects.filter(
            user=request.user):
        if request.method == 'POST':
            equipment = Equipment.objects.get(id=get_equipment)
            equipment.delete()
    return redirect('room', room_id=get_equipment.room.id)
# endregion


# region: search equipments
@login_required
def search(request):
    query = request.GET.get('query')
    residences = Residence.objects.filter(user=request.user)
    equipments = Equipment.objects.all()

    queryset = Equipment.objects.none()
    for e in equipments:
        for r in residences:
            if e.room in Room.objects.filter(residence=r):
                queryset |= Equipment.objects.filter(room=e.room)

    if not query:
        equipments = queryset
        title = "n/a"
    else:
        equipments = queryset.filter(name__icontains=query)
        title = query

    return render(request, 'search.html', {
        'equipments': equipments,
        'title': title
    })


def equipments_all(request):
    # equipments = Equipment.objects.all()
    equipments = Equipment.objects.all()

    return render(request, 'equipments_all.html', {'equipments': equipments})
# endregion
