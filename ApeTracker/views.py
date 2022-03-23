from django.http import HttpResponse
from django.shortcuts import render

from . scanScript import scanGroup

def home_view(request):
    # return HttpResponse('Hello !')
    return render(request, 'home.html')


def results(request):
    api_key = "RGAPI-983658c3-15e2-4e2a-88db-3fee8517b73e"
    inp = request.POST.get('userName')
    if " a rejoint le salon " in inp:
        inp = inp.split(" a rejoint le salon ")
        print(inp)
        for i in range(len(inp)):
            if " a rejoint le salon" in inp[i]:
                inp[i] = inp[i].replace(" a rejoint le salon","")
        
    elif "," in inp:
        inp = inp.split(",")
    
    else:
        inp = [inp]

    print(inp)

    if len(inp) == 1:
        sizeData = [0]
    if len(inp) == 2:
        sizeData = [0, 1]
    if len(inp) == 3:
        sizeData = [0, 1, 2]
    if len(inp) == 4:
        sizeData = [0, 1, 2, 3]
    if len(inp) == 5:
        sizeData = [0, 1, 2, 3, 4]
    out = scanGroup(api_key, inp)
    print(out)
    print(sizeData)
    return render(request, 'results.html', {'data':out, 'datasize':sizeData})

        
