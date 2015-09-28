#-*-coding:utf-8-*-
from django.contrib import admin
from blog.models import Tag, Comment, Catagory, Article

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
    def time_format(self, Comment):
        return Comment.create_time.strftime("%y/%m/%d")
    time_format.admin_order_field = 'create_time'
    time_format.short_description = '评论时间'

    def description(self, Comment):
        if len(Comment.content) >= 15:
            return Comment.content[:15] + '......'
        return Comment.content[:15]
    description.admin_order_field = 'content'
    description.short_description = '评论'
    list_display = ('description', 'username', 'time_format')


class ArticleAdmin(admin.ModelAdmin):
    def time_format(self, Article):
        return Article.publish_time.strftime("%y/%m/%d")
    time_format.admin_order_field = 'publish_time'
    time_format.short_description = '发表时间'

    list_display = ('title', 'author', 'time_format')

    class Media:
        js = (
            '/css/js/tinymce/tinymce.min.js',
            '/css/js/tinymce/config.js',
        )


admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Catagory, CatagoryAdmin)
admin.site.register(Article, ArticleAdmin)