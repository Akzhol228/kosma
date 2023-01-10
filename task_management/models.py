from django.db import models
from django.conf import settings
from directory.models import TypeTask
from django.db.models import Q


class Demand(models.Model):
    """Список поступивщих задач"""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type_task = models.ForeignKey(TypeTask, on_delete=models.CASCADE)
    subject = models.CharField(max_length=250)
    deadline = models.DateField()
    comment = models.TextField()
    is_archive = models.BooleanField(default=False)

    def get_responsive_distributions(self):
        return self.demanddistribution_set.filter(status__in=[2, 3, 4]).all()

    def get_count_responsive_distributions(self):
        return self.demanddistribution_set.filter(status=2).count()


class DemandFile(models.Model):
    demand = models.ForeignKey(Demand, on_delete=models.CASCADE)
    file = models.FileField(upload_to='demand_files')
    date = models.DateField(auto_now_add=True)


class DemandCompletedFile(models.Model):
    title = models.CharField(max_length=250)
    demand = models.ForeignKey(Demand, on_delete=models.CASCADE)
    file = models.FileField(upload_to='demand_completed_files')
    date = models.DateField(auto_now_add=True)


class DemandDistribution(models.Model):
    """ Распределение задач по экспертам """
    STATUS_TYPE_CHOICES = (
        (1, 'Ожидание'),
        (2, 'Отклик'),
        (3, 'Ожидание оплаты'),
        (4, 'Заказ принят')
    )

    expert = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    demand = models.ForeignKey(Demand, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.PositiveSmallIntegerField(
        choices=STATUS_TYPE_CHOICES, default=1)
    price = models.DecimalField(max_digits=5, decimal_places=0, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
