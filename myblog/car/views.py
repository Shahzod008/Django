from django.views import generic, View
from django.contrib.auth import logout, login
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

from .forms import *
from .models import *
from .utils import*

class CarHome(DataMixin, ListView):
    model = Car
    template_name = 'car/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Car.objects.filter(is_published=True).select_related('cat')

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'car/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        content = form.cleaned_data['content']
        message = ContactMessage(name=name, email=email, content=content)
        message.save()
        return redirect('home')

# Запрещает
#@login_required
class about(DataMixin, TemplateView):
    template_name = 'car/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="О сайте")
        return dict(list(context.items()) + list(c_def.items()))

class spisok_user(DataMixin, TemplateView):
    template_name = 'car/spisok_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Список пользователей")
        context['users'] = User.objects.all()  # Получаем список пользователей и добавляем его в контекст
        return dict(list(context.items()) + list(c_def.items()))

    
    
class profile(DataMixin, TemplateView):
    template_name = 'car/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Профиль")
        return dict(list(context.items()) + list(c_def.items()))


class Addpage(LoginRequiredMixin, CreateView, DataMixin):
    form_class = AddPostForm
    template_name = 'car/addpage.html'
    success_url = reverse_lazy('home')
    login_url = '/admin/'
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))


class ShowPost(DetailView, DataMixin):
    model = Car
    template_name = 'car/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))

class CarCategory(DataMixin, ListView):
    model = Car
    template_name = 'car/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Car.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat') 

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat), cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))
    

class RegisterUserForm(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'car/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')
    
class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = RegisterUserForm
    template_name = 'car/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'car/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_success_url(self):
        return reverse_lazy('home')
    
def Logout_user(request):
    logout(request)
    return redirect('home')


def pageNotFound(request, exception):
    return HttpResponseNotFound("Страница не найдена")


class ChatView(DataMixin, TemplateView):
    template_name = 'car/chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages = Message.objects.order_by('timestamp')
        form = MessageForm()
        cats = Category.objects.all()
        c_def = self.get_user_context()
        context.update({
            'messages': messages,
            'form': form,
        })
        context = {**context, **c_def}  # Объединение словарей
        return context

    def post(self, request, *args, **kwargs):
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            if self.request.user.is_authenticated:
                message.sender = self.request.user
                message.save()
                form = MessageForm()
                return HttpResponseRedirect(reverse_lazy('chat'))  # Использование reverse_lazy
            else:
                return redirect('login')
        else:
            messages = Message.objects.order_by('-timestamp')[:10]
            cats = Category.objects.all()
            c_def = self.get_user_context()
            context = {
                'messages': messages,
                'form': form,
                'cats': cats,
            }
            context.update(c_def)
            return self.render_to_response(context)


class ShowProfilePageView(DetailView):
    model = Car
    template_name = 'base/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        users = Car.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Car, id=self.kwargs['slug'])
        context['page_user'] = page_user
        return context
    

class CreateProfilePageView(CreateView):
    form_class = RegisterUserForm
    template_name = 'base/create_profile.html'
    fields = ['firs_name', 'last_name']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('tasks')