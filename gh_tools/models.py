from django.db import models
from django.template.defaultfilters import slugify


class NicheModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200)
    
    def __unicode__(self):
        return "%s - %s"%(self.name, self.description)


class ArticlePackModel(models.Model):
    packfile = models.FileField(upload_to='uploaded_articles')
    description = models.CharField('Description', max_length=150, blank=True, null=True)
    submit = models.DateField('Submit', auto_now_add=True, editable=False)
    processed = models.BooleanField('Processed')
    niche = models.ForeignKey(NicheModel, blank=True, null=True)
    
    def __unicode__(self):
        return self.description


class ArticleModel(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=150, unique=True)
    niche = models.ForeignKey(NicheModel, blank=True, null=True)
    
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(ArticleModel, self).save(*args, **kwargs)


class BlogModel(models.Model):
    address = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    niche = models.ForeignKey(NicheModel, blank=True, null=True)

    def __unicode__(self):
        return self.address

    def get_data(self):
        return {'address': self.address, 'user': self.user, 'password': self.password, 'niche': self.niche_id}
        