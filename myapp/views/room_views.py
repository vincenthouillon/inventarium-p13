from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django_tables2 import RequestConfig
from django_tables2.export.export import TableExport

from ..forms import RoomForm
from ..models import Equipment, Residence, Room
from ..tables import EquipmentTable


@login_required
def room(request, room_id):
    """Display the equipements in room.

    Arguments:
        room_id {int} -- room.id
    """
    get_room = get_object_or_404(Room, id=room_id)

    if get_room.residence in Residence.objects.filter(user=request.user):
        equipments = Equipment.objects.filter(room=get_room).order_by('name')
    else:
        raise Http404()

    return render(request, 'room/room.html', {
        'room': get_room,
        'equipments': equipments,
    })


@login_required
def room_list(request, room_id):
    """Displays an array of devices and add export in .xls.

    Arguments:
        room_id {int} -- room.id
    """
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

    return render(request, 'room/room_list.html', {
        'room': get_room,
        'equipments': equipments,
    })


@login_required
def room_add(request, residence_id):
    """Showing the add residence form.

    Arguments:
        residence_id {int} -- residence.id
    """
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

    return render(request, 'room/room_add.html', {
        'form': RoomForm,
        'residence': get_residence
    })


@login_required
def room_update(request, room_id):
    """Showing the update residence form.

    Arguments:
        room_id {int} -- room.id
    """
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

        return render(request, 'room/room_update.html', {
            'form': u_form,
            'residence': get_room.residence
        })
    else:
        raise Http404()

@login_required
def room_equipment(request, room_id, record):
    """When you click on a line in the equipment table,
    displays the details of a device.

    Arguments:
        room_id {int} -- room.id
        record {id} -- Line number for the jquery function 'To make an entire
        row in a hotspot as a link'
    """
    get_equipment = get_object_or_404(Equipment, id=record)

    if get_equipment.room.residence in Residence.objects.filter(
            user=request.user):
        equipments = get_object_or_404(Equipment, id=get_equipment.id)
    else:
        raise Http404()

    return render(request, 'equipment/equipment.html', {
        'equipment': equipments,
    })


def room_delete(request, room_id):
    """Delete room in database.

    Arguments:
        room_id {int} -- room.id
    """
    get_room = get_object_or_404(Room, id=room_id)

    # If the residence belongs to the residences of the user
    if get_room.residence in Residence.objects.filter(user=request.user):
        if request.method == 'POST':
            room = Room.objects.get(id=get_room.id)
            room.delete()
    return redirect('residence', residence_id=get_room.residence.id)
