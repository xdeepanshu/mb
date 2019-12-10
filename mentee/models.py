from django.db import models
from mb.settings.base import AUTH_USER_MODEL

class Mentee(models.Model):
    #Don't want to delete the user as it may happen that it might be referenced in mentor
    user = models.OneToOneField(AUTH_USER_MODEL, null = True, on_delete=models.SET_NULL,)
    terms_and_conditions = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Mentee"




