from django.core.management.base import BaseCommand
from parser.models import Category
import requests
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json", 
}
CATALOG_URL = 'https://static-basket-01.wbbasket.ru/vol0/data/main-menu-ru-ru-v3.json'

class Command(BaseCommand):
    help = 'Парсинг категорий Wildberries'

    def handle(self, *args, **options):

        def get_catagories():
            return requests.get(CATALOG_URL, headers=HEADERS).json()
        
        def get_data_category(catalogs_wb: dict, parent=None) -> list:
            """сбор данных категорий из каталога Wildberries"""
            for cat in catalogs_wb:
                category = Category.objects.create(
                    name = cat['name'],
                    shard= cat.get('shard', None),
                    query = cat.get('query', None),
                    url = cat['url'],
                    parent=parent
                )
                if "childs" in cat and isinstance(cat["childs"],list):
                    get_data_category(cat["childs"], parent=category)

        self.stdout.write("Парсинг категорий")
        categories = get_catagories()
        Category.objects.all().delete()
        get_data_category(categories)
        self.stdout.write("Категории сохранены")
        

        