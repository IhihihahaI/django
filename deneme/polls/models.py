from __future__ import unicode_literals
import datetime

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone

# Create your models here.

@python_2_unicode_compatible
class Question(models.Model):
    question_text = models.CharField(max_length = 200)
    pub_date = models.DateTimeField("Date Published")
    def __str__(self):
        return self.question_text
    def published_recently(self):
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days = 1)
    published_recently.admin_order_field = "pub_date"
    published_recently.boolean = True
    published_recently.short_description = "Recently published."

@python_2_unicode_compatible
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice_text = models.CharField(max_length = 200)
    votes = models.IntegerField(default = 0)
    def __str__(self):
        return self.choice_text
