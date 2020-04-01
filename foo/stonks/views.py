import time
from django.db import transaction
from django.http import HttpResponse
from random import random

from .models import Stonk


def index_view(request):
    return HttpResponse('''
        <script type="text/javascript">
            async function fluctuate() {
                document.getElementById('fluctuator').innerHTML = await (await fetch('/refresh')).text()
            }

            async function getTop() {
                document.getElementById('top').innerHTML = await (await fetch('/top')).text()
            }
        </script>
        <body>
            <button onclick="fluctuate()">Fluctuate stonks (takes a bit)</button>
            <button onclick="getTop()">Get top stonks</button>
            <div id="fluctuator"></div>
            <div id="top"></div>
        </body>
    ''')


def prepare_queryset(queryset, callback):
    def inner_decorator(f):
        def wrapped(*args, **kwargs):
            for stonk in queryset:
                kwargs['stonk'] = stonk
                f(*args, **kwargs)
            return callback()
        return wrapped
    return inner_decorator 


def refresh_view_callback():
    return HttpResponse('Stonks fluctuated')


@prepare_queryset(Stonk.objects.all(), refresh_view_callback)
@transaction.atomic()
def refresh_view(request, stonk):
    fluctuate_stonk(stonk)


def top_view_callback():
    result = ''
    for stonk in Stonk.objects.order_by('-score')[:10]:
        result += f'{stonk.name} = {stonk.value} (score {stonk.score})<br/>'
    return HttpResponse(result)


@prepare_queryset(Stonk.objects.all(), top_view_callback)
@transaction.atomic(savepoint=False)
def top_view(request, stonk):

    if stonk.value > 25000:
        bump_stonk(stonk)
    
    if stonk.value < 25000:
        hump_stonk(stonk)


def fluctuate_stonk(stonk):
    # Do not change
    print(f'Updating stonk {stonk.name}')
    stonk.value += random()
    stonk.save()
    time.sleep(0.005)


def bump_stonk(stonk):
    # Do not change
    stonk.score += 5
    stonk.save()


def hump_stonk(stonk):
    # Do not change
    stonk.score -= 2
    stonk.save()
