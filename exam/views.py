from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template import *
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import *
from django.core.urlresolvers import reverse
from django.core.exceptions import *
import models
# import forms


@login_required
def home(request):
    return HttpResponse(request.user)
