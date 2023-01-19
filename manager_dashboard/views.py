from django.views.generic.list import ListView
from task_management.mixin_views import DemandMixin
from task_management.models import Demand
from manager_dashboard.filters import DemandFilter, CallBackFilter
from main.models import CallBack
from django.db.models import Q


class DemandListView(DemandMixin, ListView):
    template_name = 'manager_dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = DemandFilter(self.request.GET, queryset=Demand.objects.all())
        return context


class CallBackListView(ListView):
    template_name = 'manager_dashboard/callback/list.html'
    model = CallBack
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = CallBackFilter(self.request.GET, queryset=CallBack.objects.all())
        return context
