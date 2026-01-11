from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, PostDetail, NewsCreate, NewsUpdate, ArticlesUpdate, NewsDelete, ArticlesDelete, SearchPostList


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем постам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostList.as_view(), name= 'post_list'),
   path('search/', SearchPostList.as_view(), name= 'search_post_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', PostDetail.as_view(), name = 'post_detail'),
   path('news/create/', NewsCreate.as_view(template_name= 'news/create.html'), name='news_create'),
   path('articles/create/', NewsCreate.as_view(template_name= 'articles/create.html'), name='articles_create'),
   path('news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
   path('articles/<int:pk>/update/', ArticlesUpdate.as_view(template_name= 'articles/create.html'), name='articles_update'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(template_name= 'news/news_delete.html'), name='news_delete' ),
   path('articles/<int:pk>/delete/', ArticlesDelete.as_view(template_name= 'articles/articles_delete.html'), name='articles_delete'),
]


