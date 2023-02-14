from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from task_management.models import DemandDistribution, Demand
from task_management.mixin_views import DemandMixin, DemandEditMixin, DemandDistributionMixin
from task_management.forms import DemandForm
from employment_portfolio.forms import CommentForm, ClaimForm
from employment_portfolio.mixin_views import CommentMixin, CommentEditMixin, ClaimMixin, ClaimEditMixin
from chat.mixin_views import MessageMixin
from accounts.models import CustomUser
from actions.mixin_views import ActionMixin, ActionContextMixin
from django.contrib import messages
from actions.models import Action


# Миксн заказа
class DemandEditMixin(DemandEditMixin):
    success_url = reverse_lazy('student_dashboard:demand_list')

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except AttributeError:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['demand_file_form_set'] = self.get_demand_file_formset()
        return context

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        form = self.form_class(request.POST, instance=instance)
        demand_file_formset = self.get_demand_file_formset(
            data=request.POST, files_data=request.FILES, instance=None)
        if form.is_valid() and demand_file_formset.is_valid():
            instance = form.save(commit=False)
            instance.student = self.request.user
            demand_files = demand_file_formset.save(commit=False)
            instance.save()
            self.save_demand_file_formset(instance, demand_files)
            return redirect('student_dashboard:demand_list')
        return render(request, 'student_dashboard/demand/form.html',
                      {'form': form})


# Список заказов
class DemandListView(DemandMixin, ActionContextMixin, ListView):
    template_name = 'student_dashboard/demand/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(student=self.request.user, is_archive=False).order_by('-id')


# Добавить заказ
class DemandCreateView(DemandMixin, DemandEditMixin, CreateView):
    template_name = 'student_dashboard/demand/form.html'


# Обновить заказ
class DemandUpdateView(DemandMixin, DemandEditMixin, UpdateView):

    def form_valid(self, form):
        super().form_valid(form)
        return JsonResponse({'success': True, 'redirect_url': reverse('student_dashboard:demand_list')})

    def form_invalid(self, form):
        form_html = render_crispy_form(form)
        return JsonResponse({'success': False, 'form_html': form_html})


# Удалить заказ
class DemandDeleteView(DemandMixin, DeleteView):
    template_name = 'student_dashboard/demand/delete.html'
    success_url = reverse_lazy('student_dashboard:demand_list')


# Удаить задания
class DemandDistributionDeleteView(DemandDistributionMixin, DeleteView):
    template_name = "task_management/demand/delete.html"
    success_url = reverse_lazy('expert_dashboard:new_task_list')


# Профиль студента
class StudentProfileView(TemplateView):
    template_name = 'student_dashboard/profile/list.html'


# Профиль студента
class StudentProfileEditView(TemplateView):
    template_name = 'student_dashboard/profile/edit.html'


# Мой баланс
class MyBalanceView(TemplateView):
    template_name = 'student_dashboard/balance/list.html'


# Выбирать эксперта
class ExpertChooseView(DemandDistributionMixin, UpdateView):
    template_name = 'student_dashboard/expert/choose.html'
    success_url = reverse_lazy('student_dashboard:demand_list')
    fields = ['status', 'phone_number', 'is_expert_selected']

    def get_initial(self):
        return { 'status': 3, 'is_expert_selected': True }

    def form_valid(self, form):
        redirect_url = super().form_valid(form)
        id = self.kwargs.get('pk')
        demand_distribution = DemandDistribution.objects.get(id=id)
        demand_distribution.demand.is_expert_selected = True
        demand_distribution.demand.save()
        return redirect_url


# Детальная информация о эксперте
class ExpertDetailView(DemandDistributionMixin, ListView):
    template_name = 'student_dashboard/expert/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['demand_distribution'] = get_object_or_404(DemandDistribution, id=self.kwargs.get('pk', None))
        return context


# Оставить комментарий
class CommentCreateView(CommentMixin, CommentEditMixin, CreateView):
    template_name = 'student_dashboard/comment/create.html'

    def form_valid(self, form):
        expert_id = self.kwargs.get('expert', None)
        expert = CustomUser.objects.get(id=expert_id)
        comment_form = CommentForm(self.request.POST)
        if comment_form.is_valid():
            form_create = comment_form.save(commit=False)
            form_create.expert = expert
            form_create.student = self.request.user
            form_create.save()
            messages.success(self.request, "Вы успешно оставили комментарий" )
            return redirect('student_dashboard:demand_list')
        return super().form_valid(form)


# Список увидомлении
class NotificationListView(ActionMixin, ListView):
    template_name = 'student_dashboard/notification/list.html'
    context_object_name = 'notifications'


# Пожаловаться
class ClaimCreateView(ClaimMixin, ClaimEditMixin, CreateView):
    template_name = 'student_dashboard/claim/create.html'

    def form_valid(self, form):
        expert_id = self.kwargs.get('pk', None)
        expert = CustomUser.objects.get(id=expert_id)
        claim_form = ClaimForm(self.request.POST)
        if claim_form.is_valid():
            form_create = claim_form.save(commit=False)
            form_create.expert = expert
            form_create.save()
            messages.success(self.request, "Вы успешно оставили жалобу" )
            return redirect('student_dashboard:demand_list')
        return super().form_valid(form)


# Список сообщений
class MessageListView(MessageMixin, ListView):
    template_name = 'student_dashboard/chat/message/list.html'
    content_type_model = DemandDistribution


# Страница архива
class DemandArchiveView(DemandMixin, UpdateView):
    template_name = 'student_dashboard/archive/create.html'
    success_url = reverse_lazy('student_dashboard:demand_list')
    fields = ('is_archive', )

    def get_initial(self):
        return { 'is_archive': True }


class DemandArchiveListView(DemandMixin, ListView):
    template_name = 'student_dashboard/archive/index.html'
    context_object_name = 'demands'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_archive=True)


# Выполненные задачи
class FinishedTaskListView(DemandDistributionMixin, ListView):
    template_name = 'student_dashboard/finished/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(status=4)

class DemandDetailView(TemplateResponseMixin, View):
    template_name = 'student_dashboard/demand/detail.html'

    def get(self, request):
        pk = request.GET.get('demand_id')
        demand_distribution_id = request.GET.get('demand_distribution')
        demand_distribution = DemandDistribution.objects.get(pk=demand_distribution_id)
        demand = Demand.objects.get(pk=pk)
        return self.render_to_response({
            'demand': demand, 'demand_distribution': demand_distribution})


class ActionDeleleteView(TemplateView ,View):
    template_name = 'student_dashboard/action/delete.html'

    def post(self, request):
        Action.objects.filter(user=request.user).delete()
        if 'create' in self.request.path:
            return JsonResponse({'success': True, 'redirect_url': reverse('student_dashboard:demand_create')})
        if 'profile' in self.request.path:
            return JsonResponse({'success': True, 'redirect_url': reverse('student_dashboard:student_profile')})
        else:
            return JsonResponse({'success': True, 'redirect_url': reverse('student_dashboard:demand_list')})
        