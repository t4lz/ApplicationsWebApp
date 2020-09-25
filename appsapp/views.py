from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import UpdateView
from .models import JobApplication, ApplicationDocument
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class IndexView(LoginRequiredMixin, generic.ListView):
    """
    Main View with all job applications, divided into ongoing and completed
    """
    template_name = 'appsapp/index.html'
    context_object_name = 'job_applications'

    def get_queryset(self):
        """Return ongoing job applications"""
        return JobApplication.objects.exclude(status__in=JobApplication.COMPLETED_STATUSES)

    def get_context_data(self, **kwargs):
        """
        Give separate querysets for ongoing and completed applications.
        """
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['completed_applications'] = JobApplication.objects.filter(status__in=JobApplication.COMPLETED_STATUSES)
        context['ongoing_applications'] = JobApplication.objects.exclude(status__in=JobApplication.COMPLETED_STATUSES)
        return context


class JobAppDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = JobApplication
    template_name = 'appsapp/details.html'

    def get_context_data(self, **kwargs):
        """
        Add the job application's files to the context
        """
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['files'] = ApplicationDocument.objects.filter(application_id=pk)
        return context

    def test_func(self):
        """
        Check that user should be able to see this applications
        """
        pk = self.kwargs['pk']
        company_name = JobApplication.objects.get(pk=pk).company_name
        groups = self.request.user.groups.all()
        return self.request.user.groups.filter(name=company_name).exists() or self.request.user.is_staff


class JobAppUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = JobApplication
    fields = ['status', 'next_step']
    template_name = 'appsapp/update.html'

    def get_context_data(self, **kwargs):
        """
        Add the job application's files to the context
        """
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['documents'] = ApplicationDocument.objects.filter(application_id=pk)
        return context

    def test_func(self):
        """
        Check that user can see this applications
        """
        pk = self.kwargs['pk']
        company_name = JobApplication.objects.get(pk=pk).company_name
        groups = self.request.user.groups.all()
        return self.request.user.groups.filter(name=company_name).exists() or self.request.user.is_staff
