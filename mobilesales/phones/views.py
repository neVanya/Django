from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, CreateView

from phones.models import Phone, CartEntry, Customer, Brand
from phones.utils import DataMixin
from templates.phones.forms import CustomerCreationForm, PhoneForm

menu = [{'title': 'Каталог', 'url_name': 'home'},
        {'title': 'Корзина покупок', 'url_name': 'shopping_cart'},
        {'title': 'Добавить товар', 'url_name': 'add_phone'},
        {'title': 'О сайте', 'url_name': 'about'}]


class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response


class AddPhone(View):
    def get(self, request):
        form = PhoneForm()
        return render(request, 'phones/html/add_phone.html', {'form': form, 'menu': menu})

    def post(self, request):
        form = PhoneForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('phones', phone_slug=form.instance.slug)

        return render(request, 'phones/html/add_phone.html', {'form': form, 'menu': menu})


def phones_view(request):
    all_phones = Phone.objects.all()

    # Устанавливаем количество телефонов на странице
    phones_per_page = 2
    paginator = Paginator(all_phones, phones_per_page)

    page = request.GET.get('page')
    try:
        phones = paginator.page(page)
    except PageNotAnInteger:
        # Если параметр страницы не является целым числом, отображаем первую страницу
        phones = paginator.page(1)
    except EmptyPage:
        # Если параметр страницы вне диапазона (например, 9999), отображаем последнюю страницу
        phones = paginator.page(paginator.num_pages)

    return render(request, 'phones/html/index.html', {'phones': phones, 'menu': menu})


class ShowPhone(DataMixin, DetailView):
    model = Phone
    template_name = 'phones/html/phone_template.html'
    slug_url_kwarg = 'phone_slug'
    context_object_name = 'phone'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Телефон')
        return {**context, **c_def}


def shopping_cart(request):
    context = {
        'menu': menu,
        'title': 'Корзина'
    }
    return render(request, 'phones/html/shopping_cart.html', context=context)


def about(request):
    context = {
        'menu': menu,
        'title': 'О сайте'
    }
    return render(request, 'phones/html/about.html', context=context)


class RegistrationView(CreateView):
    template_name = 'phones/html/register.html'
    form_class = CustomerCreationForm
    success_url = '/login/'  # URL, куда перенаправлять после успешной регистрации
    extra_context = {'menu': menu}


class LoginView(AuthLoginView):
    template_name = 'phones/html/login.html'
    success_url = '/home/'
    extra_context = {'menu': menu}


@login_required
def add_to_cart(request, phone_id):
    user = request.user

    try:
        customer = user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=user)

    phone = get_object_or_404(Phone, id=phone_id)

    cart_entry, created = CartEntry.objects.get_or_create(customer=customer, phone=phone)

    if not created:
        cart_entry.quantity += 1
        cart_entry.save()

    return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'success'})
