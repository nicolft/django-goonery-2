from django.shortcuts import get_object_or_404, render

# Create your views here.
#from django.http import HttpResponse
#from django.template import loader
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Question, Choice


class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	template_name = 'polls/detail.html'
	model = Question
	context_object_name = 'q' #default would be 'question' but I didnt follom the tutorial

class ResultsView(generic.DetailView):
	template_name = 'polls/results.html'
	model = Question
	context_object_name = 'q'

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
