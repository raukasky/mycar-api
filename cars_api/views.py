from .serializers import CarSerializer
from .models import Car
from rest_framework import generics
from django_filters import rest_framework as filters


class CarFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    min_mlg = filters.NumberFilter(field_name='mileage', lookup_expr='gte')
    max_mlg = filters.NumberFilter(field_name='mileage', lookup_expr='lte')
    min_year = filters.NumberFilter(field_name='year', lookup_expr='gte')
    max_year = filters.NumberFilter(field_name='year', lookup_expr='lte')


# Create your views here.
class CarList(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    ilter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CarFilter
