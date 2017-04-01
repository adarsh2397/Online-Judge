from django.conf.urls import url, include
from problems import views
app_name = 'problems'

urlpatterns = [
    url(r'^$', views.index,name="home"),
    url(r'^add/$', views.add_problem_form,name="add_problem"),
    url(r'^(?P<problem_id>[0-9]+)/$',views.display_problem,name="display_problem"),
    url(r'^(?P<problem_id>[0-9]+)/submit/$',views.submit_problem,name="submit"),
    url(r'^(?P<problem_id>[0-9]+)/results/(?P<run_id>[0-9]+)/$',views.display_results,name="display_results"),
    url(r'^(?P<problem_id>[0-9]+)/submissions/$',views.display_submissions,name="display_submissions"),

]