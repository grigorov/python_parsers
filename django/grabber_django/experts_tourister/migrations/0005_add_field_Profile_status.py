# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Profile.status'
        db.add_column(u'experts_tourister_profile', 'status',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Profile.status'
        db.delete_column(u'experts_tourister_profile', 'status')


    models = {
        u'experts_tourister.profile': {
            'Meta': {'object_name': 'Profile'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'url_profile': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['experts_tourister']