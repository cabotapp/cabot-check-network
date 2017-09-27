from django import forms
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from cabot.cabotapp.models import StatusCheck
from cabot.cabotapp.views import (CheckCreateView, CheckUpdateView,
                                  StatusCheckForm, base_widgets)

from .models import NetworkStatusCheck


class NetworkStatusCheckForm(StatusCheckForm):
    symmetrical_fields = ('service_set', 'instance_set')

    class Meta:
        model = NetworkStatusCheck
        fields = (
            'name',
            'host',
            'port',
            'timeout',
            'frequency',
            'active',
            'importance',
            'debounce',
        )

        widgets = dict(**base_widgets)
        widgets.update({
            'host': forms.TextInput(attrs={
                'style': 'width: 100%',
                'placeholder': 'service.arachnys.com',
            })
        })


class NetworkCheckCreateView(CheckCreateView):
    model = NetworkStatusCheck
    form_class = NetworkStatusCheckForm


class NetworkCheckUpdateView(CheckUpdateView):
    model = NetworkStatusCheck
    form_class = NetworkStatusCheckForm


def duplicate_check(request, pk):
    pc = StatusCheck.objects.get(pk=pk)
    npk = pc.duplicate()
    return HttpResponseRedirect(reverse('update-network-check', kwargs={'pk': npk}))
