from django.shortcuts import render
from .models import Gmina, Obwod
from .forms import ObwodForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError, transaction
from django.forms.models import modelformset_factory
from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect

import json

def index(request):
    obwody = Obwod.objects.all()
    paginator = Paginator(obwody, 25) # Show 25 contacts per page
    page = request.GET.get('page')

    try:
        obwodyPag = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        obwodyPag = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        obwodyPag = paginator.page(paginator.num_pages)
    context = {'obwody': obwodyPag}

    return render(request, 'wybory/obwody.html', context)

@transaction.atomic
def save(request):
    if request.method == 'POST':
        obw_id = request.POST.get('obw_id')
        ileKart = request.POST.get('ileKart')
        upr = request.POST.get('upr')
        wer = request.POST.get('wer')
        response_data = {}
        error = False

        obwody = Obwod.objects.all()
        curObwod = obwody.get(id=obw_id)

        if int(wer) < int(curObwod.wersja):
            error = True
        else:
            curObwod.wersja += 1
            curObwod.ileKart = ileKart
            curObwod.uprawnionych = upr
            curObwod.save()

        response_data = {'dict': curObwod.toDict(), 'err': error}

        return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def obwod_json(request):
    if request.method == 'POST':
        obw_id = request.POST.get('obw_id')
        response_data = {}

        obwody = Obwod.objects.all()
        obwod = obwody.get(id=obw_id)
        response_data = obwod.toDict()

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
