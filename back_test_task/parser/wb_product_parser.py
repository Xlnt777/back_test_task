import requests
import time
from .models import Category, Product
from retry import retry 
from django.core.cache import cache

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json", 
}

@retry(Exception, tries=-1, delay=0)
def scrap_page(page: int, shard: str, query: str) -> dict:
    """Сбор данных со страниц"""
    url = f'https://catalog.wb.ru/catalog/{shard}/catalog?appType=1&curr=rub' \
          f'&dest=-1257786' \
          f'&locale=ru' \
          f'&page={page}' \
          f'&sort=popular&spp=0' \
          f'&{query}' \
          
    r = requests.get(url, headers=HEADERS)
    print(f'[+] Страница {page} ')
    if r.status_code != 200 or not r.text.strip():
        raise Exception(f'Ошибка: пустой или неверный ответ от WB на странице {page}')

    try:
        return r.json()
    except Exception as e:
        raise Exception(f'Ошибка разбора JSON на странице {page}: {e} (ответ: {r.text[:100]})')
    


def get_data_from_json(json_file: dict) -> list:
    """извлекаем из json данные"""
    data_list = []
    for data in json_file['data']['products']:
        data_list.append({
            'id': data.get('id'),
            'name': data.get('name'),
            'price': int(data.get("priceU") / 100),
            'sale_price': int(data.get('salePriceU') / 100),
            'rating': data.get('reviewRating'),
            'feedbacks': data.get('feedbacks'),
            'url': f'https://www.wildberries.ru/catalog/{data.get("id")}/detail.aspx?targetUrl=BP'
        })
    
    return data_list


def parser_by_category(category_id: int, shard: str, query: str, max_pages: int = 50) -> list:
    """Парсит товары по заданной категории из БД без повторов"""

    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        print(f'[!] Категория с id={category_id} не найдена!')
        return []

    print(f'[+] Парсинг товаров категории: {category.name}')

    existing_ids = set(Product.objects.values_list('id', flat=True))

    collected = []

    for page in range(1, max_pages + 1):
        try:
            data = scrap_page(page=page, shard=shard, query=query)
            products = get_data_from_json(data)

            if not products:
                print(f'[*] Страница {page}: товаров нет. Парсинг завершен.')
                break

            for p in products:
                if p['id'] in existing_ids:
                    continue
                collected.append(Product(
                    id=p['id'],
                    category=category,
                    name=p['name'],
                    price=p['price'],
                    sale_price=p['sale_price'],
                    rating=p['rating'],
                    feedbacks=p['feedbacks'],
                    url=p['url'],
                ))

                existing_ids.add(p['id'])

        except Exception as e:
            print(f'[!] Ошибка на странице {page}: {e}')
            break

    if collected:
        try:
            Product.objects.bulk_create(collected, batch_size=500)
            print(f'[+] Сохранено {len(collected)} новых товаров.')
        except Exception as e:
            print(f'[!] Ошибка при сохранении: {e}')
    else:
        print('[*] Новых товаров не найдено.')

    return collected

       
