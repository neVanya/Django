from rest_framework.pagination import PageNumberPagination

menu = [{'title': 'Каталог', 'url_name': 'home'},
        {'title': 'Корзина покупок', 'url_name': 'shopping_cart'},
        {'title': 'Добавить товар', 'url_name': 'add_phone'},
        {'title': 'О сайте', 'url_name': 'about'}]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context

class PhoneAPIPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 5