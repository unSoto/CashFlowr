from django.core.management.base import BaseCommand
from django.db import transaction
from cashflow.models import Category, Subcategory


class Command(BaseCommand):
    help = 'Add subcategories for all categories that do not have them'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Adding missing subcategories...')

        categories = Category.objects.all()
        added_count = 0

        for category in categories:
            existing_subcats = Subcategory.objects.filter(category=category).count()

            if existing_subcats == 0:
                # Определяем подкатегории в зависимости от типа категории
                if category.type.name == 'Пополнение':
                    subcategories_to_add = self.get_income_subcategories(category)
                else:
                    subcategories_to_add = self.get_expense_subcategories(category)

                for subcat_name in subcategories_to_add:
                    Subcategory.objects.get_or_create(
                        name=subcat_name,
                        category=category
                    )
                    self.stdout.write(f'  Added subcategory "{subcat_name}" to "{category.name}"')
                    added_count += 1

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'✅ Added {added_count} subcategories successfully!'))

        # Показываем итоговую статистику
        self.stdout.write('')
        self.stdout.write('Final statistics:')
        for category in categories:
            subcats_count = Subcategory.objects.filter(category=category).count()
            self.stdout.write(f'  {category.name}: {subcats_count} subcategories')

    def get_income_subcategories(self, category):
        """Подкатегории для доходов"""
        income_subcats = {
            'Зарплата': ['Основная зарплата', 'Премия', 'Бонус', 'Овертайм'],
            'Фриланс': ['Разработка', 'Дизайн', 'Консультации', 'Поддержка'],
            'Инвестиции': ['Дивиденды', 'Проценты', 'Рост акций', 'Криптовалюта'],
            'Продажи': ['Товары', 'Услуги', 'Онлайн-продажи', 'Розничные продажи'],
            'Подарки': ['Денежные подарки', 'Наследство', 'Выигрыши', 'Компенсации'],
        }
        return income_subcats.get(category.name, ['Основная', 'Дополнительная', 'Прочая'])

    def get_expense_subcategories(self, category):
        """Подкатегории для расходов"""
        expense_subcats = {
            'Продукты': ['Супермаркет', 'Рынок', 'Доставка еды', 'Фастфуд'],
            'Транспорт': ['Общественный транспорт', 'Такси', 'Бензин', 'Парковка', 'Автосервис'],
            'Жилье': ['Аренда', 'Коммунальные услуги', 'Ремонт', 'Мебель', 'Бытовая химия'],
            'Развлечения': ['Рестораны', 'Кино', 'Концерты', 'Спорт', 'Хобби'],
            'Здоровье': ['Аптека', 'Врачи', 'Стоматология', 'Фитнес', 'Массаж'],
            'Одежда': ['Повседневная одежда', 'Деловая одежда', 'Обувь', 'Аксессуары'],
            'Техника': ['Смартфоны', 'Компьютеры', 'Бытовая техника', 'Ремонт техники'],
            'Образование': ['Книги', 'Курсы', 'Конференции', 'Сертификация'],
            'Путешествия': ['Билеты', 'Отели', 'Еда в поездке', 'Экскурсии'],
            'Автомобиль': ['Топливо', 'Обслуживание', 'Страховка', 'Штрафы'],
            'Красота': ['Парикмахерская', 'Косметика', 'Маникюр', 'СПА'],
            'Связь': ['Мобильная связь', 'Интернет', 'Телевидение', 'Почта'],
            'Домашние животные': ['Корм', 'Ветеринария', 'Аксессуары', 'Груминг'],
            'Подарки': ['Дни рождения', 'Праздники', 'Сувениры', 'Благотворительность'],
            'Благотворительность': ['Пожертвования', 'Волонтерство', 'Помощь нуждающимся'],
        }
        return expense_subcats.get(category.name, ['Основная', 'Дополнительная', 'Прочая'])
