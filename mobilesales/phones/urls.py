from django.urls import path, include, re_path
from rest_framework import routers
from phones.views import shopping_cart, about, ShowPhone, \
    RegistrationView, LoginView, add_to_cart, phones_view, CustomLogoutView, AddPhone
from phones.viewsets import BrandAPIView, PhoneViewSet

router = routers.DefaultRouter()
router.register(r'phones', PhoneViewSet, basename='phones')

urlpatterns = [
    path('', phones_view, name='home'),
    path('shopping_cart/', shopping_cart, name='shopping_cart'),
    path('register/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('add_to_cart/<int:phone_id>/', add_to_cart, name='add_to_cart'),
    path('about/', about, name='about'),
    path('phones/<slug:phone_slug>/', ShowPhone.as_view(), name='phones'),
    path('profile/', about, name='profile'),
    path('add_phone/', AddPhone.as_view(), name='add_phone'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('api/v1/', include(router.urls)),
    path('api/v1/brand', BrandAPIView.as_view()),
]
