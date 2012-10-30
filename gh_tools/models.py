from django.db import models
from django.template.defaultfilters import slugify

class ArticlePackModel(models.Model):
    packfile = models.FileField(upload_to='uploaded_articles')
    description = models.CharField('Description', max_length=150, blank=True, null=True)
    submit = models.DateField('Submit', auto_now_add=True, editable=False)
    processed = models.BooleanField('Processed')
    
class ArticleModel(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=150, unique=True)
    
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            print self.slug
        super(ArticleModel, self).save(*args, **kwargs)
