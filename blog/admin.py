from django.contrib import admin
from blog.models import BlogPost
from blog.models import Author
from blog.models import BlogPostCategory
from blog.models import BlogComment

# Register your models here.

admin.site.register(BlogPost)
admin.site.register(Author)
admin.site.register(BlogPostCategory)
admin.site.register(BlogComment)
