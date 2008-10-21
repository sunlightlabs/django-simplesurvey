from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from simplesurvey import ANONYMOUS_USER

QUESTION_TYPES = (
    ('M', 'Multiple Choice (dropdown)'),
    ('R', 'Multiple Choice (select one)'),
    ('S', 'Short Text'),
    ('L', 'Long Text'),
)

class QuestionSet(models.Model):
    """ Set of Questions that should be displayed and answered together """

    slug = models.SlugField('Slug for referring to Questionnaire',
                            unique=True)
    title = models.CharField('Title of Questionnaire', max_length=100)
    description = models.TextField('Description of Questionnaire')

    allow_anonymous = models.BooleanField('Allow anonymous users', default=True)
    allow_multiple_responses = models.BooleanField('Allow a user to complete the survey multiple times', default=True)
    
    enabled = models.BooleanField('Questionnaire is enabled', default=True)

    def __unicode__(self):
        return self.title

class Question(models.Model):

    question_set = models.ForeignKey(QuestionSet, related_name='questions')

    type = models.CharField('Question Type', max_length=1,
                            choices=QUESTION_TYPES)
    text = models.CharField('Text of Question', max_length=300)
    answer_choices = models.TextField('List of Possible Responses', blank=True)

    order = models.PositiveIntegerField('Ordering for Question upon display', default=100)
    required = models.BooleanField('Question is Required', default=True)

    class Meta:
        ordering = ['order']
        unique_together = ('question_set', 'order')

    def __unicode__(self):
        return self.text

    def get_possible_answers(self):
        """
        Return a split array of answer choices
        """
        if self.answer_choices:
            sep = getattr(settings, "SIMPLESURVEY_SEPARATOR", "|")
            choices = self.answer_choices.split(sep)
            return [c.strip() for c in choices]

class AnswerSet(models.Model):
    user = models.ForeignKey(User, related_name='answer_sets',
                             blank=True, null=True)
    question_set = models.ForeignKey(QuestionSet, related_name='answer_sets')
    date = models.DateTimeField(auto_now_add=True)

    # allow answer sets to be related to an arbitrary object
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    related_object = GenericForeignKey('content_type', 'object_id')

    def answer_for_question(self, question):
        """
        Return the answer object for a specific question
        """
        try:
            answer = self.answers.get(question=question)
            return answer
        except Answer.DoesNotExist:
            pass

    def q_and_a(self):
        return [(q, self.answer_for_question(q)) for q in self.question_set.questions.all()]

    def get_user(self):
        """
        Return the user object, or Anonymous if user is null
        """
        if self.user:
            return self.user
        return ANONYMOUS_USER

    def __unicode__(self):
        user = self.get_user()
        return u"Answers from %s" % (user.get_full_name() or user.username)

class Answer(models.Model):
    answer_set = models.ForeignKey(AnswerSet, related_name='answers')
    question = models.ForeignKey(Question, related_name='answers')
    date = models.DateTimeField(auto_now_add=True)

    text = models.TextField('Text of Answer')

    def __unicode__(self):
        return self.text
