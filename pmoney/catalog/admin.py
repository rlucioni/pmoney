from django.contrib import admin

from pmoney.catalog.models import Podcast


@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    search_fields = ('title', 'teaser')
    list_display = ('publication_date', 'title')

    fields = ('publication_date', 'title', 'teaser', 'embed_url', 'download_url', 'listened', 'created', 'modified')
    readonly_fields = ('created', 'modified')
