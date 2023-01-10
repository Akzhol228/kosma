from django.contrib.contenttypes.models import ContentType
from django.views.generic.base import View
from django.http import JsonResponse
from .forms import MessageForm
from task_management.models import DemandDistribution


class MessageCreateView(View):

    def post(self, request, *args, **kwargs):
        form = MessageForm(request.POST)
        if form.is_valid():
            content_type = ContentType.objects.get_for_model(DemandDistribution)
            obj = form.save(commit=False)
            obj.from_user = request.user
            obj.content_type = content_type
            obj.save()
            # create_action(request.user, 'Новое сообщение', obj)
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})