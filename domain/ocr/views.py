from PIL import Image
from pykospacing import Spacing
import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from domain.change.views import braille_to_list
import paho.mqtt.client as mqtt
import louis
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get('API_KEY')
# 클라이언트 초기화 (환경 변수에서 자동으로 인증 정보를 가져옴)
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-2.5-flash-lite')

# 한글 띄어쓰기 교정을 위한 Spacing
spacing = Spacing()

# MQTT 클라이언트 설정
mqttc = mqtt.Client()
mqttc.connect("broker.mqtt-dashboard.com", 1883)

@csrf_exempt
def ocr_process_view(request):
    mqttc.connect("broker.mqtt-dashboard.com", 1883)
    
    """
    multipart/form-data로 이미지를 받아 OCR 처리 후 텍스트를 반환합니다.
    """
    if request.method == 'POST':
        try:
            # 1. request.FILES에서 업로드된 이미지 파일 가져오기
            if 'image' not in request.FILES:
                return JsonResponse({"error": "요청에 이미지 파일이 없습니다"}, status=400)
            
            uploaded_file = request.FILES['image']
            device = request.POST.get('device')
            
            # 2. Pillow (PIL)를 사용하여 이미지 열기
            img = Image.open(uploaded_file)
            
            # 3. OCR 처리
            response = model.generate_content(["이미지 속의 모든 글자를 추출하여 텍스트로 정리해줘.", img])
            text = response.text.replace(" ", "")
            
            spaced_text = spacing(text)
            
            braille_chars = louis.translateString(["braille-patterns.cti", "ko-g2.ctb"], spaced_text)
           
            dot_list = braille_to_list(braille_chars)
            
            # 4. OCR 결과를 점자로 변환
            result = {
              'original_text': spaced_text,
              'posco_jamo': dot_list['one_dimension']
            }
            
            # 5. MQTT를 통해 결과 전송
            mqttc.publish(f"posco_jamo/{device}", json.dumps(result))
            
            # 6. 결과를 JSON 응답으로 반환
            json_result = {
                'original_text': spaced_text,
                'posco_jamo': dot_list['two_dimension']
            }
            return JsonResponse(json_result, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    # POST 요청이 아닐 경우 405 에러 반환
    return JsonResponse({"error": "잘못된 요청 방식입니다"}, status=405)