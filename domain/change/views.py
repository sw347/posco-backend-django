import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import louis

def braille_to_list(braille_string):
  result_list = []
  # 점자 유니코드의 시작점은 U+2800 입니다.
  braille_base_code = 0x2800

  for char in braille_string:
    # 각 문자의 유니코드 코드 포인트를 가져옵니다.
    char_code = ord(char)

    # 베이스 코드와의 차이를 이용해 점의 패턴을 계산합니다.
    pattern_value = char_code - braille_base_code

    # 6개의 점을 나타내는 리스트를 0으로 초기화합니다.
    dot_pattern = [0] * 6

    # 비트 연산을 통해 각 점의 존재 여부를 확인합니다.
    if pattern_value & 1:   # 1번 점 (2^0)
      dot_pattern[0] = 1
    if pattern_value & 2:   # 2번 점 (2^1)
      dot_pattern[1] = 1
    if pattern_value & 4:   # 3번 점 (2^2)
      dot_pattern[2] = 1
    if pattern_value & 8:   # 4번 점 (2^3)
      dot_pattern[3] = 1
    if pattern_value & 16:  # 5번 점 (2^4)
      dot_pattern[4] = 1
    if pattern_value & 32:  # 6번 점 (2^5)
      dot_pattern[5] = 1

    result_list.append(dot_pattern)

  return result_list

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