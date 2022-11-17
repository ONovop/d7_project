from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.http import Http404

class PostList(ListView):
    model = Post
    ordering = '-time_creating'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostListFiltered(ListView):
    model = Post
    ordering = '-time_creating'
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 2

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news_d.html'
    context_object_name = 'post'

class NewsCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'posts_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = Post.news
        return super().form_valid(form)

class ArticleCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'posts_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = Post.article
        return super().form_valid(form)

class NewsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    def get_object(self, queryset=None):
        initial = super(NewsUpdate, self).get_object(queryset)
        if initial.type != Post.news:
            raise Http404('Нет такой новости!')
        return initial
    template_name = 'posts_edit.html'


# Добавляем представление для изменения
class ArticleUpdate(UpdateView):
    form_class = PostForm
    model = Post
    def get_object(self, queryset=None):
        initial = super(ArticleUpdate, self).get_object(queryset)
        if initial.type != Post.article:
            raise Http404('Нет такой новости!')
        return initial
    template_name = 'posts_edit.html'


class NewsDelete(DeleteView):
    model = Post
    def get_object(self, queryset=None):
        initial = super(NewsDelete, self).get_object(queryset)
        if initial.type != Post.news:
            raise Http404('Нет такой новости!')
        return initial
    template_name = 'posts_delete.html'
    success_url = reverse_lazy('List')

class ArticleDelete(DeleteView):
    model = Post
    def get_object(self, queryset=None):
        initial = super(ArticleDelete, self).get_object(queryset)
        if initial.type != Post.article:
            raise Http404('Нет такой новости!')
        return initial
    template_name = 'posts_delete.html'
    success_url = reverse_lazy('List')
