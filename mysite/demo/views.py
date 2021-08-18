import json
from django.http import JsonResponse
import traceback


def func(a, b):
    return a / b


def index_get_r(self):

    filePath = self.GET.get("name","")

    endData = {}
    with open(filePath, encoding='utf-8') as f:
        line = f.readline()
        d = json.loads(line)
        name = d['name']
        telephone = d['telphone']
        endData['name'] = name
        endData['telephone'] = telephone
        f.close()
    #
    tracert = traceback.extract_stack()
    ss = "{} {}!" .format("hello","world")
    print(ss)

    # print(sys.exc_info())
    return JsonResponse(endData)


def index_post_r(request):

    filePath = request.POST['name']
    endData = {}
    with open(filePath, encoding='utf-8') as f:
        endData['content'] = f.read()
        f.close()
    tracert = traceback.extract_stack()
    end = traceback.format_list(tracert)
    print(end)

    # traceback.print_tb(tracert_arr[-3])
    return JsonResponse(endData)


def no_hook_fun(request):
    return JsonResponse({
        "status": "201"
    })