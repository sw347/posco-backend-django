from PIL import Image
from pykospacing import Spacing
import json
import os
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from domain.utils.formatted_data import get_formatted_braille_data
import paho.mqtt.client as mqtt
import louis
from dotenv import load_dotenv
import requests
import base64

load_dotenv()

API_KEY = os.environ.get('API_KEY')
print(API_KEY)
url = "https://api.upstage.ai/v1/document-digitization"
headers = {"Authorization": f"Bearer {API_KEY}"}

# 한글 띄어쓰기 교정을 위한 Spacing
spacing = Spacing()

# MQTT 클라이언트 설정
mqttc = mqtt.Client()
mqttc.connect("broker.mqtt-dashboard.com", 1883)

@csrf_exempt
def ocr_process_view(request):
    mqttc.connect("broker.mqtt-dashboard.com", 1883)
    
    if request.method == 'POST':
        try:
            if 'image' not in request.FILES:
                return JsonResponse({"error": "요청에 이미지 파일이 없습니다"}, status=400)
            
            uploaded_file = request.FILES['image']
            device = request.POST.get('device')
            
            if uploaded_file is None:
                return JsonResponse({"error": "업로드된 파일이 유효하지 않습니다"}, status=400)
            
            img = Image.open(uploaded_file)
            max_size = (1024, 1024)
            img.thumbnail(max_size)
            img = img.convert('L')
            
            from io import BytesIO
            img_buffer = BytesIO()
            img.save(img_buffer, format="JPEG")
            img_buffer.seek(0)
            
            files = {'document': ('image.jpeg', img_buffer.getvalue(), 'image/jpeg')}
            data = {"model": "ocr"}
            
            response = requests.post(url, headers=headers, files=files, data=data)
            
            if response.status_code != 200:
                print(f"API Error: {response.json()}")
                return JsonResponse({"error": "Upstage API 호출 실패"}, status=response.status_code)

            response_data = response.json()
            
            text = response_data.get('text', '')
            
            spaced_text = spacing(text)
            
            braille_chars = louis.translateString(["braille-patterns.cti", "ko-g2.ctb"], spaced_text)
           
            formatted_data = get_formatted_braille_data(braille_chars)
            
            print(formatted_data)
            
            result = {
              'original_text': spaced_text,
              'posco_jamo': formatted_data['mqtt_data']
            }
            
            mqttc.publish(f"posco_jamo/{device}", json.dumps(result))
            
            json_result = {
                'original_text': spaced_text,
                'posco_jamo': formatted_data['json_data']
            }
            return JsonResponse(json_result, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "잘못된 요청 방식입니다"}, status=405)