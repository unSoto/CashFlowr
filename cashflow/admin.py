from django.contrib import admin
from .models import Status, Type, Category, Subcategory, CashFlowRecord


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']
    ordering = ['name']


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']
    ordering = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'description', 'created_at']
    search_fields = ['name', 'description', 'type__name']
    list_filter = ['type', 'created_at']
    ordering = ['type__name', 'name']


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'description', 'created_at']
    search_fields = ['name', 'description', 'category__name']
    list_filter = ['category', 'created_at']
    ordering = ['category__name', 'name']


@admin.register(CashFlowRecord)
class CashFlowRecordAdmin(admin.ModelAdmin):
    list_display = ['date', 'type', 'category', 'subcategory', 'amount', 'status', 'created_at']
    search_fields = ['comment', 'type__name', 'category__name', 'subcategory__name', 'status__name']
    list_filter = ['date', 'type', 'category', 'subcategory', 'status', 'created_at']
    date_hierarchy = 'date'
    ordering = ['-date', '-created_at']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Основная информация', {
            'fields': ('date', 'amount', 'comment')
        }),
        ('Классификация', {
            'fields': ('status', 'type', 'category', 'subcategory')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'status', 'type', 'category', 'subcategory'
        )
