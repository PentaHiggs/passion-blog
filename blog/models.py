from django.db import models
from django.utils.http import urlquote, urlunquote
from django.utils import timezone

class BlogPostCategory(models.Model):
    """ Simple Model representing a blog post category """
    category_name = models.CharField(max_length=20, primary_key=True)
    def __unicode__(self):
        return self.category_name

class Author(models.Model):
    """ Simple Model representing an author """
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, primary_key=True)
    def __unicode__(self):
        return (self.name + " at " + str(self.email))

class Post(models.Model):
    """ An abstract model representing a general post """
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author)
    def return_nice_date(self):
        return self.pub_date.strftime('%B %d, %Y')

    def return_nice_timestamp(self):
        return self.pub_date.strftime('Posted at %H:%M on a %a')

    def fetch_url(self):
        date_portion = timezone.localtime(self.pub_date).strftime("/blog/%Y/%m/%d/")
        title_portion = urlquote(self.post_title)+"/"
        return date_portion + title_portion

    class Meta:
        abstract = True

class BlogPost(Post):
    """ Model represeting the specific type of blog post used in the blog app """
    post_body = models.TextField()
    categories = models.ManyToManyField(BlogPostCategory, blank=True)
    post_title = models.CharField(max_length=101, blank=False)
    def __unicode__(self):
        return ("str(self.author)" + " on " + str(self.pub_date))

    def number_of_comments(self):
        return BlogComment.objects.filter(parent_blog_post=self).count()
    
    class Meta:
        unique_together = ("pub_date", "post_title")

class BlogComment(Post):
    """ Model representing blog post comments """
    post_body = models.TextField()
    response_to = models.ForeignKey("BlogComment", blank=True, null=True)
    parent_blog_post = models.ForeignKey(BlogPost)
    post_title = models.CharField(max_length=101, default='', blank=True)
    def __unicode__(self):
        return (str(self.author) + " on " + str(self.pub_date))
