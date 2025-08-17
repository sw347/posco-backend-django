import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from hbcvt.h2b import text
# import louise

louis.loadTables('ko-g1.ctb')

@csrf_exempt
def change_text(request):
    recevied_text = request.GET.get('text', '')
    
    print("Received text 받은 글자:", recevied_text)
    
    if not recevied_text:
        return JsonResponse({'error': 'text query parameter is missing'}, stataus=400)
    
    if request.method == 'GET':
        # changed_text = braille_converter.get_braille(text)
        json_result = text(recevied_text)
        # result = extract_braille_arrays(json_result)    
        # braille_unicode = louis.translate(recevied_text)
        
        return JsonResponse({"text": braille_unicode}, status=200)