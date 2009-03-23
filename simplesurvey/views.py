from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, Http404
from simplesurvey.forms import SurveyForm
from simplesurvey.models import Answer, AnswerSet, Question, QuestionSet

#
# utility methods
#

def _object_from_contenttype(relation):
    """
    Returns an object from a content type definition in the
    form of <contenttype id>:<object pk>.
    """
    if relation:
        (ct_id, obj_id) = relation.split(":")
        ct = ContentType.objects.get(pk=ct_id)
        obj = ct.model_class().objects.get(pk=obj_id)
        obj.content_type = ct
        return obj
            
#
# view methods
#

def submit(request):
    
    if request.method == 'POST':
        
        question_set_id = request.POST.get('question_set', '')
        answer_set_id = request.POST.get('answer_set', None)
        
        try:
        
            user = request.user.is_authenticated() and request.user or None
            question_set = QuestionSet.objects.get(slug=question_set_id)
            related = _object_from_contenttype(request.POST.get('related', None))
            
            if not user and not question_set.allow_anonymous:
                raise Http404, "Anonymous users are not allowed to submit answers"
                
            if user and not question_set.allow_multiple_responses:

                qs = AnswerSet.objects.filter(question_set=question_set, user=user)
                if related:
                    qs = qs.filter(content_type=related.content_type, object_id=related.pk)
                count = qs.count()

                if count > 0 and not answer_set_id:
                    raise Http404, "This survey can be completed only once per user"
            
            form = SurveyForm(question_set, request.POST)
            
            if form.is_valid():
                
                if answer_set_id and user:
                    
                    answer_set = AnswerSet.objects.get(pk=answer_set_id)
                    
                else:
                    
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
                        
                            question = Question.objects.get(pk=k[11:], question_set=question_set)
                            
                            try:
                            
                                answer = answer_set.answers.get(question=question)
                                answer.text = v
                                
                            except Answer.DoesNotExist:
                        
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
                invalid_callback = getattr(settings, "SIMPLESURVEY_INVALID_CALLBACK", None)
                if invalid_callback:
                    return invalid_callback(request, form, question_set, related)
            
        except QuestionSet.DoesNotExist:
            raise Http404, "question set does not exist"