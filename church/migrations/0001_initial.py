# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Team'
        db.create_table(u'church_team', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=24)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=24)),
            ('members', self.gf('django.db.models.fields.CharField')(default=u'', max_length=2048)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'church', ['Team'])


    def backwards(self, orm):
        # Deleting model 'Team'
        db.delete_table(u'church_team')


    models = {
        u'church.team': {
            'Meta': {'ordering': "[u'created']", 'object_name': 'Team'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '2048'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '24'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '24'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        }
    }

    complete_apps = ['church']