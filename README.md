# 1. 가상 환경 설정

프로젝트의 의존성을 관리하기 위해 가상 환경을 활성화하는 것을 권장합니다.

### venv 가상 환경 생성 (최초 1회)

python -m venv venv

## 가상 환경 활성화

### Windows

venv\Scripts\activate

### macOS 또는 Linux

source venv/bin/activate

# 2. 의존성 설치

가상 환경을 활성화한 후, 필요한 파이썬 패키지를 설치합니다.

pip install -r requirements.txt

### macOS 또는 Linux

sudo apt install tesseract-ocr-eng tesseract-ocr-kor

# 3. 프로젝트 실행

모든 설정이 완료되면, 개발 서버를 실행하여 프로젝트를 시작할 수 있습니다.

python manage.py runserver
