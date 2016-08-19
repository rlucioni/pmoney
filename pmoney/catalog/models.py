from uuid import uuid4

from django.db import models


class Podcast(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name=_('UUID'))

    publication_date = models.DateTimeField()
    title = models.CharField(unique=True, max_length=255)
    teaser = models.TextField()
    embed_url = models.URLField(max_length=255)
    download_url = models.URLField(max_length=255)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta(object):
        ordering = ['publication_date']

    def __str__(self):
        return self.title
