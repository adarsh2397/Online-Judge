from django.conf.urls import url, include
from users import views
app_name = 'users'

urlpatterns = [
    url(r'^$', views.login_user, name="login"),
    url(r'^register/$', views.UserFormView.as_view(), name="register"),
    url(r'^logout/$', views.logout_user, name="logout"),
]