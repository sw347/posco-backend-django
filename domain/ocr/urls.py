from django.urls import path
from . import views  # views.py에서 뷰 함수를 가져옴

urlpatterns = [
    # 여기에서 separate 라우터에 해당하는 URL 패턴을 정의합니다.
    # 예: path('some-path/', views.some_view, name='some_view'),
    path('', views.ocr_process_view, name='ocr_process'),
]