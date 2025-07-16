# NFT 아트 등록 시스템

QR 코드를 스캔하고 고유번호를 입력하여 NFT 아트를 등록하는 MVP 시연 페이지입니다.

## 기능

- QR 코드 카메라 스캔
- 고유번호 입력 및 검증
- NFT 등록 및 확인
- 개인 지갑에 NFT 저장

## 기술 스택

- HTML5
- Flask (Python 웹 프레임워크)
- Bootstrap 5
- JavaScript (QR 코드 스캐닝)

## 설치 및 실행 방법

1. 필요한 패키지 설치:
   ```
   pip install -r requirements.txt
   ```

2. 애플리케이션 실행:
   ```
   python app.py
   ```

3. 웹 브라우저에서 `http://localhost:5000` 접속

## Render 배포

이 애플리케이션은 Render의 "Web Services" 옵션을 사용하여 배포할 수 있습니다.

### 배포 방법

1. Render 계정 생성 및 로그인
2. "New +" 버튼 클릭 후 "Web Service" 선택
3. GitHub 저장소 연결
4. 다음 설정 입력:
   - Name: 원하는 서비스 이름
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. "Create Web Service" 버튼 클릭

## 프로젝트 구조

```
/
├── app.py              # Flask 애플리케이션 메인 파일
├── requirements.txt    # 필요한 Python 패키지 목록
├── static/             # 정적 파일 디렉토리
│   ├── css/            # CSS 파일
│   ├── js/             # JavaScript 파일
│   └── images/         # 이미지 파일
└── templates/          # HTML 템플릿 디렉토리
    ├── index.html      # 메인 페이지
    ├── layout.html     # 기본 레이아웃
    ├── scan.html       # QR 코드 스캔 페이지
    ├── register.html   # 등록 페이지
    ├── success.html    # 등록 성공 페이지
    └── wallet.html     # 지갑 페이지
```
