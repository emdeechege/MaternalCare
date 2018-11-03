from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views, patient


urlpatterns = [
    # -- authentication views
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^medicines/$', views.medicines, name='medicines'),


    # -- general views
    url(r'^search_doctors/$', views.search_doctors, name='search_doctors'),
    url(r'^individual_doctors_page/(\d+)/(\w+)/$', views.individual_doctors_page,
        name='individual_doctors_page'),


    # -- patient views
    url(r'^edit_patient_profile/$', patient.profile_edit,
        name='edit_patient_profile'),
    # url(r'^due/$', patient.due, name='due'),

    # -- doctors views
]

# this will help to serve uploaded images on the development server
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
