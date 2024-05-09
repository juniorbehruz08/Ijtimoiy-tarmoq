from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'get_photo')
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_photo(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} height="60px">')
        else:
            return 'No photo'

    get_photo.short_description = 'photo'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'category', 'views', 'user', 'get_photo')
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title', )}


    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src={obj.photo.url} width="60px">')
        else:
            return 'No photo'

    get_photo.short_description = 'photo'


admin.site.register(Comments)
admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(AccountPhoto)
admin.site.register(Liked)
admin.site.register(Problem)
admin.site.register(Advertisement)
admin.site.register(Saved)
admin.site.register(Group)
admin.site.register(GroupMessage)
admin.site.register(Channel)
admin.site.register(ChannelMember)
admin.site.register(ChannelContent)
admin.site.register(ChannelContentComment)
