from django.db import models

class ArticlePackModel(models.Model):
    packfile = models.FileField(upload_to='uploaded_articles')
    description = models.CharField('Description', max_length=150, blank=True, null=True)
    submit = models.DateField('Submit', auto_now_add=True, editable=False)
    processed = models.BooleanField('Processed')