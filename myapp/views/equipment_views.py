from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import EquipmentForm
from ..libs.info_equipment import information
from ..models import Equipment, Residence, Room


@login_required
def equipment(request, equipment_id):
    """Display the equipments in room.

    Arguments:
        equipment_id {int} -- equipment.id
    """
    get_equipment = get_object_or_404(Equipment, id=equipment_id)

    if get_equipment.room.residence in Residence.objects.filter(
            user=request.user):
        equipments = get_object_or_404(Equipment, id=get_equipment.id)
        
        info = information(str(equipments.date_purchase),
                           str(equipments.price),
                           str(equipments.length_warranty),
                           str(equipments.category))
        if info.end_warranty > date.today():
            state_warranty = 'success'
        else:
            state_warranty = 'danger'
    else:
        raise Http404()

    return render(request, 'myapp/equipment/equipment.html', {
        'equipment': equipments,
        'lifetime': info.lifetime,
        'end_warranty': info.end_warranty,
        'wear_rate': info.wear_rate,
        'state_warranty': state_warranty,
    })


@login_required
def equipment_update(request, equipment_id):
    """Showing the add residence form.

    Arguments:
        equipment_id {int} -- equipement.id
    """
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
                return redirect('equipment', equipment_id=get_equipment.id)
        else:
            u_form = EquipmentForm(instance=get_equipment)

        return render(request, 'myapp/equipment/equipment_update.html', {
            'form': u_form,
            'equipment': get_equipment,
        })
    else:
        raise Http404()


def equipment_delete(request, equipment_id):
    """Delete equipment in database.

    Arguments:
        equipment_id {int} -- equipment.id
    """
    get_equipment = get_object_or_404(Equipment, id=equipment_id)

    # If the residence belongs to the residences of the user
    if get_equipment.room.residence in Residence.objects.filter(
            user=request.user):
        if request.method == 'POST':
            equipment = Equipment.objects.get(id=get_equipment)
            equipment.delete()
    return redirect('room', room_id=get_equipment.room.id)


@login_required
def equipment_add(request, room_id):
    """Showing the add residence form.

    Arguments:
        room_id {int} -- room.id
    """
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

        return render(request, 'myapp/equipment/equipment_add.html', {
            'form': EquipmentForm,
            'room_id': get_room,
        })

    else:
        raise Http404()


@login_required
def search(request):
    """Search result page.

    Get the name = "query" keyword in the search form in "layouts / navbar".
    The results are restricted to the residences of the user and the search is
    done on the equipment.

    Return:
        equipments {queryset} -- wanted equipments
        title {str} -- keyword search
    """
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

    return render(request, 'myapp/equipment/search.html', {
        'equipments': equipments,
        'title': title
    })


def __equipments_all(request):
    """Page needed for research."""
    equipments = Equipment.objects.all()

    return render(request, 'myapp/equipment/equipments_all.html',
                  {'equipments': equipments})
