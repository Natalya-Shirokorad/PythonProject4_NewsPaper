from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
# from .models import BaseRegisterForm
from .forms import SignUpForm
from django.urls import reverse_lazy

from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from news.models import Author
from .utils import get_group


def confirm_logout(request):
    return render(request, 'sign/confirm_logout.html')

# class BaseRegisterView(CreateView):  # 1 способ регистрация на сайте с применением models.py
#     model = User
#     form_class = BaseRegisterForm
#     success_url = '/'


class SignUpView(CreateView):   # 2 способ регистрация на сайте с применением forms.py
    model = User
    template_name = 'sign/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('index')

@login_required
def add_author_to_group(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/')

@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='premium')
    if not request.user.groups.filter(name='premium').exists():
        premium_group.user_set.add(user)
    return redirect('/')

@login_required
def my_profile(request):
    # user = request.user   #функция для перенаправления на страничку зарег. пользователя.
    context= {'is_author':request.user.groups.filter(name='authors').exists()}
               # 'if_the_author_changes':request.user.groups.filter(name='authors').exists(),}# context для проверки находится ли пользователь в группе автор.
    return render(request, 'protect/index.html', context)

# функция для прооверки относится ли зарег. пользователь к группе автор. Если такой группы нет, то создается.
@login_required
def be_author(request):
    Author.objects.get_or_create(user=request.user)
    group_authors = get_group('authors')

    if not request.user.groups.filter(name='authors').exists():
        request.user.groups.add(group_authors)
        list(messages.get_messages(request))
        messages.success(
            request, "Поздравляем! Вы стали автором!",
            extra_tags='authors'
        )

    return redirect(request.META.get('HTTP_REFERER'))

# # Функция наделения прав вносить изменения в статью
# @login_required
# def be_change(request):
#     Author.objects.get_(user=request.user)
#     if request.user.groups.filter(name='authors').exists():
#         return redirect(request.META.get('HTTP_REFERER'))

