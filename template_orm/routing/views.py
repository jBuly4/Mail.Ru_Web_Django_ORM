from django.http import HttpResponse, HttpRequest
from django.views.decorators.http import require_http_methods
import re


def simple_route(request):
    if request.method == 'GET':
        if request.body != b'':
            return HttpResponse('', status=404)
        return HttpResponse('', status=200)
    else:
        return HttpResponse('', status=405)


def slug_route(request, data):
    if (len(data) >= 1) and (len(data) <= 16):
        return HttpResponse(str(data), status=200)
    else:
        return HttpResponse('', status=404)


def sum_route(request, num1, num2):
    return HttpResponse(str(int(num1) + int(num2)))


@require_http_methods(["GET"])
def sum_get_method(request):
    num1 = request.GET.get('a', '')
    num2 = request.GET.get('b', '')

    try:
        n1 = int(num1)
        n2 = int(num2)
    except ValueError:
        return HttpResponse('', status=400)

    return HttpResponse(str(n1 + n2))


@require_http_methods(["POST"])
def sum_post_method(request):
    num1 = request.POST.get('a', '')
    num2 = request.POST.get('b', '')

    try:
        n1 = int(num1)
        n2 = int(num2)
    except ValueError:
        return HttpResponse('', status=400)

    return HttpResponse(str(n1 + n2))