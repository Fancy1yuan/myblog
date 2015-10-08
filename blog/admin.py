#-*-coding:utf-8-*-
from django.contrib import admin
from blog.models import Tag, Comment, Catagory, Article, UserProfile, Message

# Register your models here.

class TagAdmin(admin.ModelAdmin):
    def time_format(self, Catagory):
        return Catagory.create_time.strftime("%y/%m/%d")
    time_format.admin_order_field = 'create_time'
    time_format.short_description = '创建时间'

    list_display = ('name', 'time_format')


class CatagoryAdmin(admin.ModelAdmin):
    def time_format(self, Catagory):
        return Catagory.create_time.strftime("%y/%m/%d")
    time_format.admin_order_field = 'create_time'
    time_format.short_description = '创建时间'

    list_display = ('name', 'time_format')


class CommentAdmin(admin.ModelAdmin):
    # def time_format(self, Comment):
    #     return Comment.create_time.strftime("%y/%m/%d")

    def description(self, Comment):
        if len(Comment.content) >= 15:
            return Comment.content[:15] + '......'
        return Comment.content[:15]

    # time_format.admin_order_field = 'create_time'
    # time_format.short_description = '评论时间'
    description.admin_order_field = 'content'
    description.short_description = '评论'
    list_display = ('description', 'username') # , 'time_format')


class ArticleAdmin(admin.ModelAdmin):

    def time_format(self, Article):
        return Article.publish_time.strftime("%y/%m/%d")

    time_format.admin_order_field = 'publish_time'
    time_format.short_description = '发表时间'

    list_display = ('title', 'author', 'time_format')

    class Media:
        js = (
            '/static/js/tinymce/tinymce.min.js',
            '/static/js/tinymce/config.js',
        )


class MessageAdmin(admin.ModelAdmin):

    def time_format(self, Message):
        return Message.create_time.strftime("%y/%m/%d")

    def description(self, Message):
        if len(Message.message) >= 15:
            return Message.message[:15] + '......'
        return Message.message[:15]

    time_format.admin_order_field = 'create_time'
    time_format.short_description = '创建时间'
    description.admin_order_field = 'message'
    description.short_description = '留言'

    list_display = ['name', 'description', 'time_format']


admin.site.register(UserProfile)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Catagory, CatagoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Message, MessageAdmin)