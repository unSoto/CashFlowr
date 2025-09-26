from django import forms
from django.core.exceptions import ValidationError
from .models import CashFlowRecord, Category, Subcategory, Status, Type


class CashFlowRecordForm(forms.ModelForm):
    """Форма для создания и редактирования записей ДДС"""

    class Meta:
        model = CashFlowRecord
        fields = ['date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control', 'id': 'id_type'}),
            'category': forms.Select(attrs={'class': 'form-control', 'id': 'id_category'}),
            'subcategory': forms.Select(attrs={'class': 'form-control', 'id': 'id_subcategory'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'date': 'Дата операции',
            'status': 'Статус',
            'type': 'Тип',
            'category': 'Категория',
            'subcategory': 'Подкатегория',
            'amount': 'Сумма (руб.)',
            'comment': 'Комментарий',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Фильтрация категорий по типу (если тип выбран)
        if 'type' in self.data:
            try:
                type_id = int(self.data.get('type'))
                self.fields['category'].queryset = Category.objects.filter(type_id=type_id)
            except (ValueError, TypeError):
                self.fields['category'].queryset = Category.objects.none()
        elif self.instance.pk and self.instance.type:
            self.fields['category'].queryset = Category.objects.filter(type=self.instance.type)
        else:
            self.fields['category'].queryset = Category.objects.none()

        # Фильтрация подкатегорий по категории (если категория выбрана)
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                self.fields['subcategory'].queryset = Subcategory.objects.none()
        elif self.instance.pk and self.instance.category:
            self.fields['subcategory'].queryset = Subcategory.objects.filter(category=self.instance.category)
        else:
            self.fields['subcategory'].queryset = Subcategory.objects.none()

    def clean(self):
        """Валидация всей формы"""
        cleaned_data = super().clean()
        type_obj = cleaned_data.get('type')
        category_obj = cleaned_data.get('category')
        subcategory_obj = cleaned_data.get('subcategory')

        # Проверка соответствия категории типу
        if type_obj and category_obj and category_obj.type != type_obj:
            raise ValidationError(
                "Выбранная категория не соответствует типу операции. "
                "Пожалуйста, выберите категорию, соответствующую типу."
            )

        # Проверка соответствия подкатегории категории
        if category_obj and subcategory_obj and subcategory_obj.category != category_obj:
            raise ValidationError(
                "Выбранная подкатегория не соответствует категории. "
                "Пожалуйста, выберите подкатегорию, соответствующую категории."
            )

        return cleaned_data


class StatusForm(forms.ModelForm):
    """Форма для управления статусами"""

    class Meta:
        model = Status
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class TypeForm(forms.ModelForm):
    """Форма для управления типами"""

    class Meta:
        model = Type
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class CategoryForm(forms.ModelForm):
    """Форма для управления категориями"""

    class Meta:
        model = Category
        fields = ['name', 'type', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class SubcategoryForm(forms.ModelForm):
    """Форма для управления подкатегориями"""

    class Meta:
        model = Subcategory
        fields = ['name', 'category', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
