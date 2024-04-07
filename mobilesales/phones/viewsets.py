from django.forms import model_to_dict
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from phones.models import Phone, Customer, Brand
from phones.permissions import IsAdminOrReadOnly
from phones.serializers import PhoneSerializers, PhoneDetailSerializers
from phones.utils import PhoneAPIPagination


class PhoneViewSet(viewsets.ModelViewSet):
    pagination_class = PhoneAPIPagination
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializers
    permission_classes = (IsAdminOrReadOnly, )

    @action(methods=['get'], detail=False)
    def brand(self, request):
        brand = Brand.objects.all()
        return Response({'brand': [f'Наименование - {br.Name}' for br in brand]})

    @action(methods=['get'], detail=True)
    def brand(self, request, pk=None):
        brand = Brand.objects.filter(pk=pk).first()
        if brand:
            return Response({'brand': [f'Наименование - {br.Name}' for br in brand]})
        else:
            return Response({'brand': 'Брэнд не найдена'})

    def get_queryset(self):
        brand = self.request.GET.get('brand', '')
        if brand:
            return Phone.objects.filter(brand_id=brand)
        else:
            return Phone.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PhoneDetailSerializers
        return PhoneSerializers


class BrandAPIView(APIView):
    def get(self, request):
        brand = Brand.objects.all().values()
        return Response({'brand': list(brand)})

    def post(self, request):
        new_brand = Brand.objects.create(
            name=request.data['name']
        )
        return Response({'brand': model_to_dict(new_brand)})
