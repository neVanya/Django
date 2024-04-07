from rest_framework import serializers
from phones.models import Phone


class PhoneSerializers(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ('brand', 'model', 'price', 'stock_quantity', 'photo', 'slug',)


class PhoneDetailSerializers(serializers.ModelSerializer):
    brand_name = serializers.SerializerMethodField()

    class Meta:
        model = Phone
        fields = '__all__'

    def get_brand_name(self, obj):
        return f'{obj.brand.name}'