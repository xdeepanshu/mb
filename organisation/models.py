from django.db import models

#https://goodcode.io/articles/django-singleton-models/

class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()

"""
Want to restrict the organisation to contain only one row
"""

class Organisation(SingletonModel):
    name = models.CharField(max_length=100, verbose_name="Name of the organisation")
    description = models.TextField(verbose_name="Description of the organisation")
    website_url = models.URLField(verbose_name="Website of the organisation", blank=True)
    facebook_url = models.URLField(blank=True, verbose_name="Facebook URL")
    twitter_url = models.URLField(blank=True, verbose_name="Twitter URL")
    linkedin_url = models.URLField(blank=True)
    
    def __str__(self):
        return self.name

