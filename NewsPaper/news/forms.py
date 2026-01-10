from django import forms
from .models import Post, Author, Category
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=10, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Напишите текст записи'})),

    categorys = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Используем чекбоксы для выбора нескольких категорий
        label='Категории',
        required=True  # Можно ли создать пост без категории? Если да, то False. Если нет, то True.
    )
    # author = forms.ModelChoiceField(
    #     queryset=Author.objects.all(),
    #     label='Автор',
    #     empty_label='любой'
    # )

    class Meta:
        model = Post
        fields = ['title', 'text', 'categorys']

        labels = {
            'title': 'Заголовок',
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        title = cleaned_data.get("title")

        if title == text:
            raise ValidationError(
                "Название не должно быть идентично тексту статьи или новости."
            )
        title = self.cleaned_data["title"]
        if title[0].islower():
            raise ValidationError(
                "Название должно начинаться с заглавной буквы."
            )
        return cleaned_data