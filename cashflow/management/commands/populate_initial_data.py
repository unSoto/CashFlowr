from django.core.management.base import BaseCommand
from django.db import transaction
from cashflow.models import Status, Type, Category, Subcategory


class Command(BaseCommand):
    help = 'Populate initial reference data for the cash flow application'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset existing data before populating',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('Resetting existing data...')
            Subcategory.objects.all().delete()
            Category.objects.all().delete()
            Type.objects.all().delete()
            Status.objects.all().delete()

        self.stdout.write('Creating initial reference data...')

        # Создание статусов
        statuses_data = [
            {'name': 'Бизнес', 'description': 'Операции, связанные с бизнесом'},
            {'name': 'Личное', 'description': 'Личные расходы и доходы'},
            {'name': 'Налог', 'description': 'Налоговые платежи и возвраты'},
        ]

        statuses = []
        for status_data in statuses_data:
            status, created = Status.objects.get_or_create(
                name=status_data['name'],
                defaults={'description': status_data['description']}
            )
            if created:
                self.stdout.write(f'  Created status: {status.name}')
            statuses.append(status)

        # Создание типов операций
        types_data = [
            {'name': 'Пополнение', 'description': 'Поступление денежных средств'},
            {'name': 'Списание', 'description': 'Расход денежных средств'},
        ]

        types = []
        for type_data in types_data:
            operation_type, created = Type.objects.get_or_create(
                name=type_data['name'],
                defaults={'description': type_data['description']}
            )
            if created:
                self.stdout.write(f'  Created type: {operation_type.name}')
            types.append(operation_type)

        # Получение созданных типов
        income_type = types[0]  # Пополнение
        expense_type = types[1]  # Списание

        # Создание категорий для доходов
        income_categories_data = [
            {'name': 'Зарплата', 'description': 'Заработная плата и премии'},
            {'name': 'Фриланс', 'description': 'Доходы от фриланса и подработок'},
            {'name': 'Инвестиции', 'description': 'Дивиденды, проценты от инвестиций'},
            {'name': 'Продажи', 'description': 'Доходы от продажи товаров/услуг'},
            {'name': 'Подарки', 'description': 'Денежные подарки и помощь'},
        ]

        income_categories = []
        for cat_data in income_categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                type=income_type,
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(f'  Created income category: {category.name}')
            income_categories.append(category)

        # Создание категорий для расходов
        expense_categories_data = [
            {'name': 'Продукты', 'description': 'Еда и продукты питания'},
            {'name': 'Транспорт', 'description': 'Транспортные расходы'},
            {'name': 'Жилье', 'description': 'Аренда, коммунальные услуги'},
            {'name': 'Развлечения', 'description': 'Рестораны, кино, хобби'},
            {'name': 'Здоровье', 'description': 'Медицина, спорт, аптека'},
            {'name': 'Одежда', 'description': 'Одежда, обувь, аксессуары'},
            {'name': 'Техника', 'description': 'Электроника, гаджеты'},
            {'name': 'Образование', 'description': 'Курсы, книги, обучение'},
            {'name': 'Путешествия', 'description': 'Отдых, поездки'},
            {'name': 'Автомобиль', 'description': 'Топливо, обслуживание, страховка'},
            {'name': 'Красота', 'description': 'Парикмахерская, косметика'},
            {'name': 'Связь', 'description': 'Телефон, интернет'},
            {'name': 'Домашние животные', 'description': 'Корм, ветеринария'},
            {'name': 'Подарки', 'description': 'Подарки для других'},
            {'name': 'Благотворительность', 'description': 'Пожертвования'},
        ]

        expense_categories = []
        for cat_data in expense_categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                type=expense_type,
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(f'  Created expense category: {category.name}')
            expense_categories.append(category)

        # Создание подкатегорий для расходов
        subcategories_data = [
            # Продукты
            {'name': 'Супермаркет', 'category': expense_categories[0]},
            {'name': 'Рынок', 'category': expense_categories[0]},
            {'name': 'Доставка еды', 'category': expense_categories[0]},

            # Транспорт
            {'name': 'Общественный транспорт', 'category': expense_categories[1]},
            {'name': 'Такси', 'category': expense_categories[1]},
            {'name': 'Бензин', 'category': expense_categories[1]},
            {'name': 'Парковка', 'category': expense_categories[1]},

            # Жилье
            {'name': 'Аренда', 'category': expense_categories[2]},
            {'name': 'Коммунальные услуги', 'category': expense_categories[2]},
            {'name': 'Ремонт', 'category': expense_categories[2]},

            # Развлечения
            {'name': 'Рестораны', 'category': expense_categories[3]},
            {'name': 'Кино', 'category': expense_categories[3]},
            {'name': 'Концерты', 'category': expense_categories[3]},
            {'name': 'Спорт', 'category': expense_categories[3]},

            # Здоровье
            {'name': 'Аптека', 'category': expense_categories[4]},
            {'name': 'Врачи', 'category': expense_categories[4]},
            {'name': 'Стоматология', 'category': expense_categories[4]},
            {'name': 'Фитнес', 'category': expense_categories[4]},

            # Одежда
            {'name': 'Повседневная одежда', 'category': expense_categories[5]},
            {'name': 'Деловая одежда', 'category': expense_categories[5]},
            {'name': 'Обувь', 'category': expense_categories[5]},

            # Техника
            {'name': 'Смартфоны', 'category': expense_categories[6]},
            {'name': 'Компьютеры', 'category': expense_categories[6]},
            {'name': 'Бытовая техника', 'category': expense_categories[6]},

            # Образование
            {'name': 'Книги', 'category': expense_categories[7]},
            {'name': 'Курсы', 'category': expense_categories[7]},
            {'name': 'Конференции', 'category': expense_categories[7]},

            # Связь
            {'name': 'Мобильная связь', 'category': expense_categories[11]},
            {'name': 'Интернет', 'category': expense_categories[11]},
            {'name': 'Телевидение', 'category': expense_categories[11]},
        ]

        for subcat_data in subcategories_data:
            subcategory, created = Subcategory.objects.get_or_create(
                name=subcat_data['name'],
                category=subcat_data['category']
            )
            if created:
                self.stdout.write(f'  Created subcategory: {subcategory.name}')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('✅ Initial data populated successfully!'))
        self.stdout.write('')
        self.stdout.write('Summary:')
        self.stdout.write(f'  - Statuses: {Status.objects.count()}')
        self.stdout.write(f'  - Types: {Type.objects.count()}')
        self.stdout.write(f'  - Categories: {Category.objects.count()}')
        self.stdout.write(f'  - Subcategories: {Subcategory.objects.count()}')
        self.stdout.write('')
        self.stdout.write('You can now start the development server with:')
        self.stdout.write('  python manage.py runserver')
