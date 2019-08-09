# https://django-tables2.readthedocs.io/en/latest/
import django_tables2 as tables

from ..models import Equipment


class TruncatedTextColumn(tables.Column):
    """A Column to limit to 100 characters and add an ellipsis."""
    def render(self, value):
        if len(value) > 102:
            return value[0:99] + '...'
        return str(value)


class EquipmentTable(tables.Table):
    """Define au custom Table class."""
    name = tables.Column(verbose_name="Equipement", attrs={
                         'td': {'class': 'text-capitalize'}})
    brand = tables.Column()
    model = tables.Column()
    length_warranty = tables.Column(visible=False)
    price = tables.Column()
    note = tables.Column(visible=False)
    note2 = TruncatedTextColumn(accessor=('note'), exclude_from_export=True)

    class Meta:
        model = Equipment
        attrs = {'class': 'table table2'}
        row_attrs = {'class': 'clickable-row',
                     'data-href': lambda record: record.pk}
        exclude = ['id', 'room', 'is_active', 'picture', 'invoice', 'manual']
        template_name = 'django_tables2/bootstrap.html'
