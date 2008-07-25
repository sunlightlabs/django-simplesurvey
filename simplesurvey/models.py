from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

QUESTION_TYPES = (
    ('M', 'Multiple Choice'),
    ('S', 'Short Text'),
    ('L', 'Long Text'))

class QuestionSet(models.Model):
    """ Set of Questions that should be displayed and answered together """

    slug = models.SlugField('Slug for referring to Questionnaire',
                            primary_key=True)
    title = models.CharField('Title of Questionnaire', max_length=100)
    description = models.TextField('Description of Questionnaire')

class Question(models.Model):

    question_set = models.ForeignKey(QuestionSet, related_name='questions')

    type = models.CharField('Question Type', max_length=1,
                            choices=QUESTION_TYPES)
    text = models.CharField('Text of Question', max_length=300)
    answer_choices = models.TextField('List of Possible Responses', blank=True)

    order = models.PositiveIntegerField('Ordering for Question upon display')
    required = models.BooleanField('Question is Required', default=True)

    class Meta:
        ordering = ['order']
        unique_together = ('question_set', 'order')

class AnswerSet(models.Model):
    user = models.ForeignKey(User, related_name='answer_sets')
    question_set = models.ForeignKey(QuestionSet, related_name='answer_sets')
    date = models.DateTimeField(auto_now_add=True)

    # allow answer sets to be related to an arbitrary object
    related_content_type = models.ForeignKey(ContentType, null=True)
    related_object_id = models.PositiveIntegerField(null=True)
    related_object = GenericForeignKey('related_content_type',
                                       'related_object_id')


class Answer(models.Model):
    answer_set = models.ForeignKey(AnswerSet, related_name='answers')
    question = models.ForeignKey(Question, related_name='answers')

    text = models.TextField('Text of Answer')
