# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ArticleModel.slug'
        db.alter_column('gh_tools_articlemodel', 'slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=150))

    def backwards(self, orm):

        # Changing field 'ArticleModel.slug'
        db.alter_column('gh_tools_articlemodel', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True))

    models = {
        'gh_tools.articlemodel': {
            'Meta': {'object_name': 'ArticleModel'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '150'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'gh_tools.articlepackmodel': {
            'Meta': {'object_name': 'ArticlePackModel'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'packfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'submit': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['gh_tools']