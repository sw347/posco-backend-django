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

# 1. Tesseract 실행 파일 경로 설정 (Windows 사용자만 해당)
# 설치 경로에 따라 달라질 수 있으니 확인하세요.
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
config_string = '--psm 6 --oem 2'
spacing = Spacing()

@csrf_exempt
def ocr_process_view(request):
    """
    multipart/form-data로 이미지를 받아 OCR 처리 후 텍스트를 반환합니다.
    """
    if request.method == 'POST':
        try:
            # 1. request.FILES에서 업로드된 이미지 파일 가져오기
            # 'image'라는 이름은 HTML <input type="file"> 태그의 name 속성이나
            # Postman의 form-data 필드 이름과 일치해야 합니다.
            if 'image' not in request.FILES:
                return JsonResponse({"error": "요청에 이미지 파일이 없습니다"}, status=400)
            
            uploaded_file = request.FILES['image']
            
            # 2. Pillow (PIL)를 사용하여 이미지 열기
            img = Image.open(uploaded_file)
            # image_np = np.array(img)
            # gray_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
            # _, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

            # kernel = np.ones((2, 2), np.uint8)
            # dilated_image = cv2.dilate(binary_image, kernel, iterations=1)

            # 3. OCR 처리
            text = pytesseract.image_to_string(img, lang='eng+kor', config=config_string).replace(" ", "")
            
            spaced_text = spacing(text)
            
            # 4. 결과를 JSON 응답으로 반환
            return JsonResponse({"ocr_text": spaced_text}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    # POST 요청이 아닐 경우 405 에러 반환
    return JsonResponse({"error": "잘못된 요청 방식입니다"}, status=405)