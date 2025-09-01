import pytesseract
from PIL import Image
from pykospacing import Spacing
import json
import base64
import io
import cv2
import os
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from domain.change.views import braille_to_list
import paho.mqtt.client as mqtt
import time
import louis
import requests
import base64

# Tesseract 실행 파일 경로 설정
# 설치 경로에 따라 달라질 수 있으니 확인하세요.

api_key = "up_f3T75NfooG06f5fcVr7hwEfzrH5cp"
url = "https://api.upstage.ai/v1/document-digitization"
headers = {"Authorization": f"Bearer {api_key}"}

# Linux 또는 macOS
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# 클라이언트 초기화 (환경 변수에서 자동으로 인증 정보를 가져옴)
# genai.configure(api_key=r"AIzaSyDw-mGVaxH_BicNB1Uy-SEk2MtX0hVGU3Q")

# AIzaSyDw-mGVaxH_BicNB1Uy-SEk2MtX0hVGU3Q

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
            start_time = time.time()
            
            # 1. request.FILES에서 업로드된 이미지 파일 가져오기
            if 'image' not in request.FILES:
                return JsonResponse({"error": "요청에 이미지 파일이 없습니다"}, status=400)
            
            uploaded_file = request.FILES['image']
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            
            files = {'document': uploaded_file.open()}
            data = {"model": "ocr"}
            
            response = requests.post(url, headers=headers, files=files, data=data)
            
            if response.status_code != 200:
                print(f"API Error: {response.json()}")
                return JsonResponse({"error": "Upstage API 호출 실패"}, status=response.status_code)

            # API 응답에서 텍스트 추출
            response_data = response.json()
            # Upstage OCR API의 응답 구조는 'text' 키에 전체 텍스트가 포함됩니다.
            text = response_data.get('text', '')
            
            # 2. Pillow (PIL)를 사용하여 이미지 열기
            # img = Image.open(uploaded_file)
            # img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            
            # 1. 흑백 이미지로 변환
            # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # 2. 이진화 (글자와 배경을 명확하게 분리)
            # _, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            
            # 3. (선택적) 이미지 확대 - 글자가 작을 경우에만 사용
            # resized_binary_image = cv2.resize(binary_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

            # Tesseract 설정
            # config_string = '--psm 6 --oem 1'

            # 3. OCR 처리
            # response = client.text_detection(image=image)
            # texts = response.text_annotations
            # text = pytesseract.image_to_string(resized_binary_image , lang='eng+kor', config=config_string).replace(" ", "")
            # text = model.generate_content(["이미지 속의 모든 글자를 추출하여 텍스트로 정리해줘.", img])
            
            spaced_text = spacing(text)
            
            braille_chars = louis.translateString(["braille-patterns.cti", "ko-g1.ctb"], spaced_text)
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Total processing time: {elapsed_time:.4f} seconds")
            
            dot_list = braille_to_list(braille_chars)
            
            # 4. OCR 결과를 점자로 변환
            result = {
              'original_text': spaced_text,
              'posco_jamo': dot_list['one_dimension']
            }
            
            # 5. MQTT를 통해 결과 전송
            mqttc.publish("posco_jamo", json.dumps(result))
            
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