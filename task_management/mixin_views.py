from django.forms.models import inlineformset_factory
from .models import Demand, DemandDistribution, DemandFile, DemandCompletedFile
from .forms import DemandForm, DemandDistributionForm, DemandFileForm, DemandCompletedFileForm


class DemandMixin:
    template_name = 'task_management/demand/form.html'
    model = Demand
    context_object_name = "demands"
    paginate_by = 10

    @staticmethod
    def get_demand_file_formset(instance=None, data=None, files_data=None):
        demand_file_form_set = inlineformset_factory(
            Demand,
            DemandFile,
            form=DemandFileForm,
            extra=0, can_delete=True)
        return demand_file_form_set(data, files_data, instance=instance, prefix='files')

    @staticmethod
    def save_demand_file_formset(instance, demand_files):
        for demand_file in demand_files:
            demand_file.demand = instance
            demand_file.save()


    @staticmethod
    def get_demand_completed_file_formset(instance=None, data=None, files_data=None):
        demand_completed_file_form_set = inlineformset_factory(
            Demand,
            DemandCompletedFile,
            form=DemandCompletedFileForm,
            extra=0, can_delete=True)
        return demand_completed_file_form_set(data, files_data, instance=instance, prefix='files')


    @staticmethod
    def save_demand_completed_file_formset(instance, demand_completed_files):
        for demand_completed_file in demand_completed_files:
            demand_completed_file.demand = instance
            demand_completed_file.save()


class DemandEditMixin:
    form_class = DemandForm


class DemandDistributionMixin:
    model = DemandDistribution
    context_object_name = "demand_distributions"
    paginate_by = 10


class DemandDistributionEditMixin:
    form_class = DemandDistributionForm
