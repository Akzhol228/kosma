from django.contrib.contenttypes.models import ContentType
from .models import Message


class MessageMixin:
    model = Message
    context_object_name = 'messages'
    content_type_model = None

    def dispatch(self, request, *args, **kwargs):
        room = self.kwargs.get('room')
        room_split = room.split("_")
        self.room_split_0 = room_split[0]
        self.room_split_1 = room_split[1]
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        if self.content_type_model:
            content_type = ContentType.objects.get_for_model(self.content_type_model)
            qs = qs.filter(content_type=content_type, object_id=self.room_split_1)
            qs.exclude(from_user=self.request.user).update(is_read=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_split_0'] = self.room_split_0
        context['room_split_1'] = self.room_split_1
        return context