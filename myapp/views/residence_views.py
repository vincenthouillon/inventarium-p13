from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import ResidenceForm
from ..models import Residence, Room


@login_required
def homepage(request):
    """Display the user account page."""
    qs_residences = Residence.objects.filter(
        user=request.user).order_by('name')

    return render(request, 'residence/homepage.html',
                  {'residences': qs_residences, })


@login_required
def residence(request, residence_id):
    """Display the rooms.

    Arguments:
        residence_id {int} -- residence.id
    """
    get_residence = get_object_or_404(
        Residence, id=residence_id, user=request.user)
    rooms = Room.objects.filter(residence=get_residence).order_by('name')

    return render(request, 'residence/residence.html', {
        'rooms': rooms,
        'residence': get_residence,
    })


@login_required
def residence_add(request):
    """Add residence user's in database."""
    if request.method == 'POST':
        form = ResidenceForm(request.POST)
        if form.is_valid():
            home = form.save(commit=False)
            home.user = request.user  # The logged user
            home.save()
            return redirect('residence/homepage')
    else:
        form = ResidenceForm()
    return render(request, 'residence/residence_add.html', {
        'form': form,
        'user': request.user
    })


@login_required
def residence_update(request, residence_id):
    """Update residence.

    Arguments:
        residence_id {int} -- residence.id
    """
    get_residence = get_object_or_404(
        Residence, pk=residence_id, user=request.user)

    if request.method == "POST":
        u_form = ResidenceForm(request.POST, instance=get_residence)
        if u_form.is_valid():
            u_form.save()
            messages.success(
                request, f'Votre résidence a bien été mise à jour')
            return redirect('residence/homepage')
    else:
        u_form = ResidenceForm(instance=get_residence)

    return render(request, 'residence/residence_update.html',
                  {'u_form': u_form})


def residence_delete(request, residence_id):
    """Delete residence in database.

    Arguments:
        residence_id {int} -- residence.id
    """
    if request.method == 'POST':
        residence = get_object_or_404(
            Residence, pk=residence_id, user=request.user)
        residence.delete()
    return redirect('residence/homepage')
