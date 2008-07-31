from copy import deepcopy
from django import forms
from django.contrib.contenttypes.models import ContentType

class SurveyForm(forms.Form):
    
    def __init__(self, question_set, *args, **kwargs):
        
        related_object = kwargs.get('related_object', None)
        if related_object:
            del kwargs['related_object']
        
        super(self.__class__, self).__init__(*args, **kwargs)
        
        for question in question_set.questions.all():
            
            name = "answer_for_%i" % question.id
            field = self._get_field(question)
            
            if field:
                self.base_fields[name] = field
                
        if related_object:
            ct = ContentType.objects.get_for_model(related_object)
            related = u"%i:%s" % (ct.id, related_object.pk)
            self.base_fields['related'] = forms.CharField(widget=forms.HiddenInput, initial=related)
            
        self.base_fields['question_set'] = forms.CharField(widget=forms.HiddenInput, initial=question_set.pk)
        self.fields = deepcopy(self.base_fields)
        
    def _get_field(self, question):
        if question.type == 'M':
            choices = [('','')]
            choices += [(c, c) for c in question.get_possible_answers()]
            return forms.ChoiceField(choices=choices, label=question.text, required=question.required)
        elif question.type == 'S':
            return forms.CharField(label=question.text, required=question.required)
        elif question.type == 'L':
            return forms.CharField(widget=forms.Textarea, label=question.text, required=question.required)
    