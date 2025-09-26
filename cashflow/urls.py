from django.urls import path
from . import views

app_name = 'cashflow'

urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),

    # CRUD операции для записей ДДС
    path('record/create/', views.record_create, name='record_create'),
    path('record/<int:pk>/edit/', views.record_edit, name='record_edit'),
    path('record/<int:pk>/delete/', views.record_delete, name='record_delete'),

    # AJAX endpoints для динамической фильтрации
    path('api/categories-by-type/', views.get_categories_by_type, name='categories_by_type'),
    path('api/subcategories-by-category/', views.get_subcategories_by_category, name='subcategories_by_category'),

    # Управление справочниками
    path('reference/', views.reference_data, name='reference_data'),
]
