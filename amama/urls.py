
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from mama.views import PaymentView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^payments/', include('pesapal.urls')),
    url(r"buy", PaymentView.as_view(), name="payment"),
    url(r'', include('mama.urls')),

]
