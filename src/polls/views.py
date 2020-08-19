from django.shortcuts import get_object_or_404, render

# Create your views here.
#from django.http import HttpResponse
#from django.template import loader
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Question, Choice


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #template = loader.get_template('polls/index.html')
    context = { #this is a dictionarp
    	'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
	q = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', {'q':q})


def results(request, question_id):
	q = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {'q':q})

def vote(request, question_id):
	q = get_object_or_404(Question, pk=question_id)
	#1. try to get the selected choice and increment its votes attribute
	#2. return an httpresponse
	try:
		selected_choice = q.choice_set.get(pk=request.POST["choice"])
	except(Choice.DoesNotExist, KeyError):
		return render(request, 'polls/detail.html', {'q':q, 'error_message':"You didn't select an option."})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:results', args=(q.id,)))
