管理员帐号：admin
          admin

简短说明：
    1 数据库使用的是SQLite3
    2 用户认证基本使用了Django自带的认证系统，用户的Model是继承了AbstractUser，添加了头像 QQ 电话 和简介。
    3 模板来自www.competethemes.com/apex-live-demo，非常精简


功能：
    1 用户可注册
    2 所有人都可以浏览全部的文章，发表文章需注册登陆
    3 可以使用关键字搜索，仅限于对文章标题的搜索
    4 可以使用分类和标签对文章进行查找
    5 给后台和发表文章添加了Tinymce富文本编辑器


运行： `python manage.py runserver`