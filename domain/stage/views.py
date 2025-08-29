from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from domain.utils.dot_to_list import braille_to_list
import louis
from .models.level import Level
from .models.words import Words
from .models.region import Region

def to_dot(w, model = "ko-g1.ctb"):
   braille_chars = louis.translateString(["braille-patterns.cti", model], w)
   return {
      "word": w,
      "dot": braille_to_list(braille_chars)["two_dimension"]
   }


@csrf_exempt
def get_stages(request):
  if request.method == 'GET':
    level_text = request.GET.get('level')
    region_text = request.GET.get('region', 'ko_kr')
    
    region_text = region_text.lower()

    if not level_text:
      return JsonResponse({'error': 'level query parameter is missing'}, status=400)
    
    level = Level(level_text.lower())
    region = Region(region_text)
        
    try:  
        words = []
        if region is Region.KO_KR: 
          match level:
              case Level.EASY:
                  words = Words.korean_alphabets
              case Level.NORMAL:
                  words = Words.full_korean_character_list
              case Level.HARD:
                  words = Words.full_korean_word_list
              case _:
                  words = []
        else:
            match level:
              case _:
                  words = Words.alphabet

        match region:
           case Region.KO_KR:
              table = "ko-g1.ctb"        
           case Region.EN_US:
              table = "en-us-g1.ctb"

        wordWithDots = list(map(lambda w: to_dot(w, model=table), words))

        json_result = {
            'size': len(wordWithDots),
            'stages': wordWithDots
        }
        return JsonResponse(json_result, status = 200)
    except Exception as e:
      error_details = {
          "error": "An error occurred during Braille translation.",
          "message": str(e)
      }
        
      return JsonResponse(error_details, status=500, safe=False)