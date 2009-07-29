from copy import deepcopy
from django import forms
from django.contrib.contenttypes.models import ContentType

class SurveyForm(forms.Form):
    
    def __init__(self, question_set, *args, **kwargs):
        """
        Create a form object from a question set.
        Method takes and option related_object keyword argument that relates
        the survey to an instance of a Django model.
        """
        
        # get related_object and remove from kwargs that are passed to super.__init__
        related_object = kwargs.get('related_object', None)
        try:
            del kwargs['related_object']
        except KeyError:
            pass
        
        # pull possible answer_set parameter from kwargs
        answer_set = kwargs.get('answer_set', None)
        try:
            del kwargs['answer_set']
        except KeyError:
            pass
        
        # call super constructor to setup initial fields of form
        super(self.__class__, self).__init__(*args, **kwargs)
        
        # iterate over questions and create corresponding form fields
        for question in question_set.questions.order_by('order'):
            
            name = "answer_for_%i" % question.id
            field = self._get_field(question)

            if field:
                self.base_fields[name] = field
                
        # add related object if one was specified
        if related_object:
            ct = ContentType.objects.get_for_model(related_object)
            related = u"%i:%s" % (ct.id, related_object.pk)
            self.base_fields['related'] = forms.CharField(widget=forms.HiddenInput, initial=related)
            if answer_set:
                self.data['related'] = related
        
        # populate form with answer_set data if it exists
        if answer_set:
            self.base_fields['answer_set'] = forms.CharField(widget=forms.HiddenInput, initial=answer_set.pk)
            self.data['answer_set'] = answer_set.pk
            self.is_bound = True
            for question, answer in answer_set.q_and_a():
                name = "answer_for_%i" % question.id
                self.data[name] = answer.text
                
        # add question set
        self.base_fields['question_set'] = forms.CharField(widget=forms.HiddenInput, initial=question_set.slug)
        if answer_set:
            self.data['question_set'] = question_set.slug
        
        # copy basefields to fields, duplicate of funcationality in super.__init__
        self.fields = deepcopy(self.base_fields)
        
    def _get_field(self, question):
        """
        Create a form field based on a question.
        """
        
        # multiple choice field (select)
        if question.type == 'M':
            
            choices = [('','')] + [(c, c) for c in question.get_possible_answers()]
            return forms.ChoiceField(
                label=question.text,
                required=question.required,
                widget=forms.Select(attrs={'class':'select_choice_field'}),
                choices=choices)
                
        # multiple choice field (radio)
        if question.type == 'R':

            choices = [(c, c) for c in question.get_possible_answers()]
            return forms.ChoiceField(
                label=question.text,
                required=question.required,
                widget=forms.RadioSelect(attrs={'class':'radio_choice_field'}),
                choices=choices)
        
        # multiple choice field (checkbox)
        if question.type == 'C':
          
            choices = [(c, c) for c in question.get_possible_answers()]
            return forms.MultipleChoiceField(
                label=question.text,
                required=question.required,
                widget=forms.CheckboxSelectMultiple(attrs={'class':'checkbox_choice_field'}),
                choices=choices)
            
        # short text field
        elif question.type == 'S':
            
            return forms.CharField(
                label=question.text,
                required=question.required,
                widget=forms.TextInput(attrs={'class':'short_text_field'}))
            
        # long text field
        elif question.type == 'L':
            
            return forms.CharField(
                label=question.text,
                required=question.required,
                widget=forms.Textarea(attrs={'class':'long_text_field'}))