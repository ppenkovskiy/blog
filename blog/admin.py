from django.contrib import admin
from .models import Post, Tag, Comment


# class PostAdmin(admin.ModelAdmin):
#     list_filter = ('tag', 'date')
#     list_display = ('title', 'date')
#     prepopulated_fields = {'slug': ('title',)}
#
#
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('user_name', 'post', 'text',)


# admin.site.register(Post, PostAdmin)
admin.site.register(Post)

admin.site.register(Tag)
admin.site.register(Comment)
# admin.site.register(Comment, CommentAdmin)

