from django.conf.urls import include, url

urlpatterns = [
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.jwt')),             #JWT view
    url(r'^organisation/', include('organisation.urls')),
]