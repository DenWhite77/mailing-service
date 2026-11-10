from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.core.cache import cache

from .models import Client, Message, Mailing, MailingAttempt
from .forms import ClientForm, MessageForm, MailingForm
from .services import send_mailing


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            is_manager = user.groups.filter(name='Менеджеры').exists()

            if is_manager:
                mailings = Mailing.objects.all()
                attempts = MailingAttempt.objects.all()
                clients = Client.objects.all()
            else:
                mailings = Mailing.objects.filter(owner=user)
                attempts = MailingAttempt.objects.filter(mailing__owner=user)
                clients = Client.objects.filter(owner=user)

            context['total_mailings'] = mailings.count()
            context['total_attempts'] = attempts.count()
            context['successful_attempts'] = attempts.filter(status='success').count()
            context['total_clients'] = clients.count()

        return context


# ============================================================
# CRUD ДЛЯ ПОЛУЧАТЕЛЕЙ (CLIENT)
# ============================================================

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'mailing/client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Client.objects.all()
        return Client.objects.filter(owner=user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list')

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'mailing/client_confirm_delete.html'
    success_url = reverse_lazy('mailing:client_list')

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


# ============================================================
# CRUD ДЛЯ СООБЩЕНИЙ (MESSAGE)
# ============================================================

class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Message.objects.all()
        return Message.objects.filter(owner=user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:message_list')

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


# ============================================================
# CRUD ДЛЯ РАССЫЛОК (MAILING)
# ============================================================

class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        user = self.request.user
        cache_key = f'mailing_list_{user.id}'

        # Пытаемся взять из кеша
        queryset = cache.get(cache_key)
        if queryset is None:
            if user.groups.filter(name='Менеджеры').exists():
                queryset = list(Mailing.objects.all())
            else:
                queryset = list(Mailing.objects.filter(owner=user))
            # Кешируем на 5 минут
            cache.set(cache_key, queryset, timeout=300)
            print(f'[CACHE] Список рассылок пользователя {user.id} из БД')
        else:
            print(f'[CACHE] Список рассылок пользователя {user.id} из Redis')

        return queryset


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        cache.delete(f'mailing_list_{self.request.user.id}')
        return response


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    context_object_name = 'mailing'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)

    def form_valid(self, form):
        response = super().form_valid(form)
        cache.delete(f'mailing_list_{self.request.user.id}')
        return response


class MailingSendView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = request.user
        if user.groups.filter(name='Менеджеры').exists():
            mailing = get_object_or_404(Mailing, pk=pk)
        else:
            mailing = get_object_or_404(Mailing, pk=pk, owner=user)

        send_mailing(mailing.pk)
        return redirect('mailing:mailing_detail', pk=pk)


# ============================================================
# СПИСОК ПОПЫТОК (MAILING ATTEMPT)
# ============================================================

class AttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = 'mailing/attempt_list.html'
    context_object_name = 'attempts'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return MailingAttempt.objects.all()
        return MailingAttempt.objects.filter(mailing__owner=user)
