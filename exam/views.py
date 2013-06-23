from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template import *
from django.shortcuts import render_to_response, render
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import *
from django.core.urlresolvers import reverse
from django.core.exceptions import *
import models
import datetime
import json
# import forms

class Test:
    current_tests = {}
    """A test class representing the test a user is taking"""
    def __init__(self, user):
        self.user = user
        self.score = 0
        # Ten questions in Ten minutes
        self.num_questions = 10
        self.duration = datetime.timedelta(seconds=10)
        self.num_solved_questions = 0
        self.questions_seen = []
        self.last_question, self.second_last_question = None, None
        self.current_difficulty = 4
        self.start_time = datetime.datetime.now()
        self.finish_time = self.start_time + self.duration
        self.current_question = self.get_new_question(self.current_difficulty)

    def get_new_question(self, difficulty):
        q = models.Question.objects.filter(difficulty=difficulty).order_by('?')[0]
        while q.pk in self.questions_seen:
            q = models.Question.objects.filter(difficulty=difficulty).order_by('?')[0]
        return q

    def solve_current(self, answer):
        if self.current_question.correct_option == answer:
            self.score += self.current_question.difficulty
            self.current_question.correct = True
        else:
            self.current_question.correct = False
        self.num_solved_questions += 1
        self.questions_seen.append(self.current_question.pk)
        self.second_last_question, self.last_question = self.last_question, self.current_question
        if self.second_last_question and self.last_question:
            if self.second_last_question.correct and self.last_question.correct:
                self.current_difficulty = min(10, self.current_difficulty + 1)
            elif (not self.second_last_question.correct) and (not self.last_question.correct):
                self.current_difficulty = max(1, self.current_difficulty - 1)
        if not self.finished:
            self.current_question = self.get_new_question(self.current_difficulty)

    @property
    def finished(self):
        return datetime.datetime.now() > self.finish_time or self.num_solved_questions == self.num_questions

    @classmethod
    def user_check_current_test(cls, user):
        return cls.current_tests[user.username] if user.username in cls.current_tests else None

    @classmethod
    def get_test(cls, user):
        #don't use setdefault here
        if user.username not in cls.current_tests:
            cls.current_tests[user.username] = Test(user)
        return cls.current_tests[user.username]


@login_required
def home(request):
    mydict = {}
    mydict['test_running'] = Test.user_check_current_test(request.user)
    return render_to_response('home.html', mydict, context_instance=RequestContext(request))


@login_required
def continue_test(request):
    if request.method == 'GET':
        raise Http404
    test = Test.get_test(request.user)
    if 'option_checked' in request.POST and not test.finished:
        test.solve_current(int(request.POST.get('option_checked')))
    result_dict = dict(finish_time='new Date("%s")' % test.finish_time.ctime(), num_solved_questions=test.num_solved_questions, num_questions=test.num_questions)
    if test.finished:
        result_dict['finished'] = True
        result_dict['score'] = test.score
        del Test.current_tests[request.user.username]
    else:
        result_dict['current_question'] = test.current_question.to_dict()
    return HttpResponse(json.dumps(result_dict))
