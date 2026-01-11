
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author
from datetime import datetime
from .filters import PostFilter
from django.utils import timezone
from django.urls import reverse_lazy
from .forms import PostForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class PostList(ListView):
    model = Post
    post_type = None
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-time_in'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 10  # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
    # С помощью super() мы обращаемся к родительским классам
    # и вызываем у них метод get_context_data с теми же аргументами,
    # что и были переданы нам.
    # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
    # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
    # Добавим ещё одну пустую переменную,
    # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_posts'] = "Самые свежие новости в мире спорта смотрите на нашем сайте"
    # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельной статье или новости
    model = Post
    # Используем другой шаблон — post.html
    template_name = 'news_id.html'
    # Название объекта, в котором будет выбранный пользователем пост(статья или новость)
    context_object_name = 'news_id'


class NewsCreate(CreateView):
    model = Post
    form_class = PostForm
    # success_url = reverse_lazy('post_list') # Либо функцию в модель Пост def get_absolute_url(self) для возвращения на страницу новостей
    template_name = 'news/create.html'

    def form_valid(self, form):
        # 1. Создаем объект из данных формы, но в БД еще не отправляем
        # (поля формы заполнены, но author и article_or_news еще пустые)
        post = form.save(commit=False)

        # 2. Теперь мы можем вручную «допилить» объект
        post.article_or_news = 'NE'  # Назначаем тип
        post.author = Author.objects.get(user=self.request.user)  # Назначаем автора

        # 3. И вот теперь, когда все обязательные поля заполнены,
        # сохраняем объект в базу данных окончательно
        post.save()

        return super().form_valid(form)

class ArticlesCreate(CreateView):
    model = Post
    form_class = PostForm
    # success_url = reverse_lazy('post_list') # Либо функцию в модель Пост def get_absolute_url(self) для возвращения на страницу новостей
    template_name = 'articles/create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.article_or_news = 'AR'
        post.author = Author.objects.get(user=self.request.user)  # Назначаем автора
        post.save()
        return super().form_valid(form)

class NewsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/create.html'

class ArticlesUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'articles/create.html'

class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')

class ArticlesDelete(DeleteView):
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('post_list')

class SearchPostList(PostList):
    template_name = 'search.html'
    paginate_by = 5  # вот так мы можем указать количество записей на странице
