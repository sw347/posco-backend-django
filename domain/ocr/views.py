import pytesseract
from PIL import Image
from pykospacing import Spacing
import json
import base64
import io
import cv2
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from domain.change.views import braille_to_list

# 1. Tesseract 실행 파일 경로 설정
# 설치 경로에 따라 달라질 수 있으니 확인하세요.

# Windows
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Linux 또는 macOS
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
config_string = '--psm 6 --oem 1'
spacing = Spacing()

@csrf_exempt
def ocr_process_view(request):
    """
    multipart/form-data로 이미지를 받아 OCR 처리 후 텍스트를 반환합니다.
    """
    if request.method == 'POST':
        try:
            # 1. request.FILES에서 업로드된 이미지 파일 가져오기
            if 'image' not in request.FILES:
                return JsonResponse({"error": "요청에 이미지 파일이 없습니다"}, status=400)
            
            uploaded_file = request.FILES['image']
            
            # 2. Pillow (PIL)를 사용하여 이미지 열기
            img = Image.open(uploaded_file)

            # 3. OCR 처리
            text = pytesseract.image_to_string(img, lang='eng+kor', config=config_string).replace(" ", "")
            
            spaced_text = spacing(text)
            
            # 4. 결과를 JSON 응답으로 반환
            return JsonResponse({"ocr_dots": braille_to_list(spaced_text)}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    # POST 요청이 아닐 경우 405 에러 반환
    return JsonResponse({"error": "잘못된 요청 방식입니다"}, status=405)