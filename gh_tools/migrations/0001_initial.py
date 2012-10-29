# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ArticlePackModel'
        db.create_table('gh_tools_articlepackmodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('packfile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('submit', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('processed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('gh_tools', ['ArticlePackModel'])


    def backwards(self, orm):
        # Deleting model 'ArticlePackModel'
        db.delete_table('gh_tools_articlepackmodel')


    models = {
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