from django.db.models import fields
import django_filters
from django_filters import DateFilter



from .models import Order

class orderFilter(django_filters.FilterSet):
    start = DateFilter(field_name='date_created', lookup_expr= 'gte')
    end = DateFilter(field_name='date_created', lookup_expr= 'lte')
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']


        