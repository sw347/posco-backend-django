from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from domain.utils.dot_to_list import braille_to_list
import louis

@csrf_exempt
def change_text(request):    
    if request.method == 'GET':
        recevied_text = request.GET.get('text')
        
        if not recevied_text:
            return JsonResponse({'error': 'text query parameter is missing'}, stataus=400)
        
    try:
        dot_result = louis.translateString(["braille-patterns.cti", "ko-g1.ctb"], recevied_text)
        result = braille_to_list(dot_result)
        print(result)
        return JsonResponse({"dots": result}, status = 200)

    except Exception as e:
        error_details = {
            "error": "An error occurred during Braille translation.",
            "message": str(e)
        }
        return JsonResponse(error_details, status=500, safe=False)