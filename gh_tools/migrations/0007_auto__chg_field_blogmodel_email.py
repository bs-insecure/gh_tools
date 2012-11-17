# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'BlogModel.email'
        db.alter_column('gh_tools_blogmodel', 'email', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

    def backwards(self, orm):

        # Changing field 'BlogModel.email'
        db.alter_column('gh_tools_blogmodel', 'email', self.gf('django.db.models.fields.CharField')(default=None, max_length=100))

    models = {
        'gh_tools.articlemodel': {
            'Meta': {'object_name': 'ArticleModel'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gh_tools.NicheModel']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '150'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'gh_tools.articlepackmodel': {
            'Meta': {'object_name': 'ArticlePackModel'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gh_tools.NicheModel']", 'null': 'True', 'blank': 'True'}),
            'packfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'submit': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'gh_tools.blogmodel': {
            'Meta': {'object_name': 'BlogModel'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gh_tools.NicheModel']", 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'gh_tools.nichemodel': {
            'Meta': {'object_name': 'NicheModel'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['gh_tools']