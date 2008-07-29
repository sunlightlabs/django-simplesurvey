from django.contrib import admin
from simplesurvey.models import Answer, AnswerSet, Question, QuestionSet

# Questions
    
class QuestionInline(admin.TabularInline): 
    model = Question
    extra = 5
    ordering = ('order',)

class QuestionSetAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = [QuestionInline]
    
admin.site.register(QuestionSet, QuestionSetAdmin)

# Answers

class AnswerInline(admin.TabularInline):
    model = Answer
    ordering = ('question.order',)
    
class AnswerSetAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    
admin.site.register(AnswerSet, AnswerSetAdmin)