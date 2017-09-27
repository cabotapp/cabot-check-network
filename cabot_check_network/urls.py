from django.conf.urls import url

from .views import (NetworkCheckCreateView, NetworkCheckUpdateView,
                    duplicate_check)

urlpatterns = [

    url(r'^networkcheck/create/',
        view=NetworkCheckCreateView.as_view(),
        name='create-network-check'),

    url(r'^networkcheck/update/(?P<pk>\d+)/',
        view=NetworkCheckUpdateView.as_view(),
        name='update-network-check'),

    url(r'^networkcheck/duplicate/(?P<pk>\d+)/',
        view=duplicate_check,
        name='duplicate-network-check')

]
