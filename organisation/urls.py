from django.urls import path
from organisation.views import OrganisationView

urlpatterns = [
    path('', OrganisationView.as_view())
]

