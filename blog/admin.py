from django.contrib import admin
from .models import Post, Comment
# summernote library used to style post text
from django_summernote.admin import SummernoteModelAdmin


# register post model on admin portal
@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    # adding more funtionality to the admin portal
    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content']
    list_filter = ('status', 'created_on')
    # prepopulating the slug field based on the title
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('name', 'email', 'body')
    # Allows an admin to approve comments
    actions = ['approve_comments']

    # function allowing admin to set approved to True
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
