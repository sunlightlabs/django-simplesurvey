from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^submit/$', 'simplesurvey.views.submit', name="survey_submit"),
)