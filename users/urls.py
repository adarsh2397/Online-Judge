from django.conf.urls import url, include
from users import views
app_name = 'users'

urlpatterns = [
    url(r'^$', views.login_user, name="login"),
    url(r'^register/$', views.UserFormView.as_view(), name="register"),
    url(r'^logout/$', views.logout_user, name="logout"),
    url(r'^additional/$', views.AdditionalDetailsView.as_view(), name="additional"),
    url(r'^additional/update/$',views.my_view,name="additional-update"),
    url(r'^profile/(?P<user_id>[0-9]+)/$',views.profile_display,name="profile_display"),
]