from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active  = models.BooleanField(default=True)

    class Meta:
        abstract = True

class File(models.Model):
    name = models.CharField(max_length=25, null=True, blank=True)
    image = models.FileField(blank=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)
