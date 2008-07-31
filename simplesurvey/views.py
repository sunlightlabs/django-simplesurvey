from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from simplesurvey.forms import SurveyForm
from simplesurvey.models import Answer, AnswerSet, Question, QuestionSet

def submit(request):
    
    if request.method == 'POST':
        
        question_set_id = request.POST.get('question_set', '')
        
        try:
            
            question_set = QuestionSet.objects.get(pk=question_set_id)
            form = SurveyForm(question_set, request.POST)
            
            user = request.user.is_authenticated() and request.user or None
            
            related = request.POST.get('related', None)
            if related:
                (ct_id, obj_id) = related.split(":")
                ct = ContentType.objects.get(pk=ct_id)
                related = ct.model_class().objects.get(pk=obj_id)
            
            if form.is_valid():
                
                answer_set = AnswerSet(
                    question_set=question_set,
                    user=user
                )
                
                if related:
                    answer_set.related_object = related
                    
                answer_set.save()
                
                for k, v in form.cleaned_data.items():
                    
                    if k.startswith("answer_for_"):
                        
                        try:
                        
                            question = Question.objects.get(pk=k[11:])
                            
                            answer = Answer(
                                question=question,
                                answer_set=answer_set,
                                text=v
                            )
                            
                            answer.save()
                            
                        except Question.DoesNotExist:
                            pass
                            
                return HttpResponseRedirect(
                    getattr(settings, 'SIMPLESURVEY_COMPLETE_REDIRECT', '/survey/complete/'))
                
            else:
                pass
            
        except QuestionSet.DoesNotExist:
            pass