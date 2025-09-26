from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Status, Type, Category, Subcategory, CashFlowRecord
from .forms import CashFlowRecordForm


def index(request):
    """Главная страница с таблицей записей ДДС и фильтрами"""
    # Получение параметров фильтрации
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    status_id = request.GET.get('status')
    type_id = request.GET.get('type')
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')

    # Базовый queryset
    records = CashFlowRecord.objects.select_related(
        'status', 'type', 'category', 'subcategory'
    ).order_by('-date', '-created_at')

    # Применение фильтров
    if date_from:
        records = records.filter(date__gte=date_from)
    if date_to:
        records = records.filter(date__lte=date_to)
    if status_id:
        records = records.filter(status_id=status_id)
    if type_id:
        records = records.filter(type_id=type_id)
    if category_id:
        records = records.filter(category_id=category_id)
    if subcategory_id:
        records = records.filter(subcategory_id=subcategory_id)

    # Пагинация
    paginator = Paginator(records, 20)  # 20 записей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Получение данных для фильтров
    statuses = Status.objects.all()
    types = Type.objects.all()
    categories = Category.objects.select_related('type').all()
    subcategories = Subcategory.objects.select_related('category').all()

    context = {
        'page_obj': page_obj,
        'statuses': statuses,
        'types': types,
        'categories': categories,
        'subcategories': subcategories,
        'current_filters': {
            'date_from': date_from,
            'date_to': date_to,
            'status': status_id,
            'type': type_id,
            'category': category_id,
            'subcategory': subcategory_id,
        }
    }

    return render(request, 'cashflow/index.html', context)


def record_create(request):
    """Создание новой записи ДДС"""
    if request.method == 'POST':
        form = CashFlowRecordForm(request.POST)
        if form.is_valid():
            record = form.save()
            messages.success(request, 'Запись успешно создана!')
            return redirect('cashflow:index')
    else:
        form = CashFlowRecordForm()

    context = {
        'form': form,
        'title': 'Создание записи ДДС'
    }
    return render(request, 'cashflow/record_form.html', context)


def record_edit(request, pk):
    """Редактирование записи ДДС"""
    record = get_object_or_404(CashFlowRecord, pk=pk)

    if request.method == 'POST':
        form = CashFlowRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись успешно обновлена!')
            return redirect('cashflow:index')
    else:
        form = CashFlowRecordForm(instance=record)

    context = {
        'form': form,
        'record': record,
        'title': 'Редактирование записи ДДС'
    }
    return render(request, 'cashflow/record_form.html', context)


def record_delete(request, pk):
    """Удаление записи ДДС"""
    record = get_object_or_404(CashFlowRecord, pk=pk)

    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Запись успешно удалена!')
        return redirect('cashflow:index')

    context = {
        'record': record,
        'title': 'Удаление записи ДДС'
    }
    return render(request, 'cashflow/record_confirm_delete.html', context)


def get_categories_by_type(request):
    """AJAX endpoint для получения категорий по типу"""
    type_id = request.GET.get('type_id')
    if type_id:
        categories = Category.objects.filter(type_id=type_id).values('id', 'name')
        return JsonResponse(list(categories), safe=False)
    return JsonResponse([], safe=False)


def get_subcategories_by_category(request):
    """AJAX endpoint для получения подкатегорий по категории"""
    category_id = request.GET.get('category_id')
    if category_id:
        subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
        return JsonResponse(list(subcategories), safe=False)
    return JsonResponse([], safe=False)


def reference_data(request):
    """Страница управления справочниками"""
    context = {
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.select_related('type').all(),
        'subcategories': Subcategory.objects.select_related('category').all(),
    }
    return render(request, 'cashflow/reference_data.html', context)
