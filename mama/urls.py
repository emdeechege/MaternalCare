from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views, patient, trimester, doctor, forum


urlpatterns = [
    # -- authentication views
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^book_appointment/$', views.book_appointment, name='book_appointment'),
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
    url(r'^doctors_dashboard/$', doctor.dashboard, name='doctors_dashboard'),



    # --trimester views
    url(r'^trimester1/$', trimester.trimester1,
        name='trimester1'),
    url(r'^trimester2/$', trimester.trimester2,
        name='trimester2'),
    url(r'^trimester3/$', trimester.trimester3,
        name='trimester3'),

    # ---forum views
    url(r'^blogpost/$', forum.create_post, name='create_post'),
    url(r'^comment/', forum.add_comment, name='comment'),
    url(r'^forum/$', forum.forum, name='forum'),

]


# this will help to serve uploaded images on the development server
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
