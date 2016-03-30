import datetime
from django.db.models import Avg, Sum, F, Max, Count
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View, TemplateView
from django.http import HttpResponse
from django.views.generic.base import ContextMixin
from django.views.generic.dates import YearMixin
from project.app1.models import Some1
from .forms import Some2FactoryForm, Some1Form, FormForm


class Some1ListView(ListView):
    model = Some1
    template_name = 'list.html'
    form = Some1Form

    def get_context_data(self, **kwargs):
        context = super(Some1ListView, self).get_context_data(**kwargs)
        context['val1'] = 'abc'
        context['form'] = Some2FactoryForm  # FORM-FACTORY
        context['form_form'] = self.form
        context['result'] = Some1.objects \
            .extra(select={'day': 'date(app1_some1.date)'}) \
            .values('day') \
            .annotate(Count('id'))
        return context

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        # request.POST._mutable = True
        # form.data['field1'] = 'bbb'
        # form.data['int_field'] = '2'
        # form.data['date'] = ''
        if form.is_valid():
            obj = form.save()
            return redirect(obj)
        return render(request, self.template_name, context={'form_form': form})


class Some1DetailView(DetailView):
    template_name = 'detail.html'

    def __init__(self):
        super(Some1DetailView, self).__init__()
        self.model = Some1


def simple_view(request, pk):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    # return HttpResponse(html)
    return render(request, 'list.html', {"foo": "bar"})


class SimpleView(ContextMixin, View):
    formset = formset_factory(FormForm, extra=3, can_delete=True)
    # formset = modelformset_factory(Some1, fields=("field1", "id"))(queryset=Some1.objects.all())
    #         (initial=[
    #     {
    #         'your_name': 'aaaa',
    #         'data_fine': 'date',
    #     }
    # ])

    def get_context_data(self, **kwargs):
        context = super(SimpleView, self).get_context_data(**kwargs)
        context['formset'] = self.formset
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, 'formset.html', context)

    def post(self, request, *args, **kwargs):
        formset = self.formset(request.POST)
        if formset.is_valid():
            pass
        return render(request, 'formset.html', {'formset': formset})
