from django.shortcuts import get_object_or_404, render

# Create your views here.
#from django.http import HttpResponse
#from django.template import loader
from django.http import Http404

from .models import Question


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
	try:
		q = Question.objects.get(pk=1)
	except:
		raise Http404("Poll does not exist.")
	context = {'q':q}
	return render(request, 'polls/vote.html', context)