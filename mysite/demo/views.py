import json
from django.http import JsonResponse


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
    return JsonResponse(endData)


def index_post_r(request):

    filePath = request.POST['name']
    endData = {}
    with open(filePath, encoding='utf-8') as f:
        endData['content'] = f.read()
        f.close()
    return JsonResponse(endData)


def no_hook_fun(request):
    return JsonResponse({
        "status": "201"
    })