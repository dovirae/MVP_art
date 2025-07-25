from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import uuid
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# JSON 파일 경로 설정
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
NFT_DATA_FILE = os.path.join(DATA_DIR, 'nfts.json')
WALLET_DATA_FILE = os.path.join(DATA_DIR, 'wallets.json')

# XRP 테스트 지갑 ID 미리 생성
TEST_WALLET_ID = "rP3X7h7oC7vX9k9z8b9m9n9p9q9r9s9t9u"

# 데이터 디렉토리 생성
try:
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"DATA_DIR created at: {DATA_DIR}")
except Exception as e:
    print(f"Error creating DATA_DIR: {e}")

# JSON 파일에서 데이터 로드
def load_nfts():
    if os.path.exists(NFT_DATA_FILE):
        with open(NFT_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def load_wallets():
    if os.path.exists(WALLET_DATA_FILE):
        with open(WALLET_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    # 기본 테스트 지갑 데이터
    return {
        TEST_WALLET_ID: [
            {
                "id": "nft001",
                "name": "DOVIARAE 아트픽셀001",
                "image": "images/nft1.png",
                "registered_at": "2025-07-17 08:30:00"
            },
            {
                "id": "4324325200111223",
                "name": "DOVIARAE 아트픽셀",
                "image": "images/4324325200111223.png",
                "registered_at": "2025-07-17 09:00:00"
            }
        ]
    }

# JSON 파일에 데이터 저장
def save_nfts(data):
    try:
        # 디렉토리가 존재하는지 한 번 더 확인
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(NFT_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"NFT data saved to {NFT_DATA_FILE}")
        print(f"Saved NFT data: {data}")
    except Exception as e:
        print(f"Error saving NFT data: {e}")

def save_wallets(data):
    try:
        # 디렉토리가 존재하는지 한 번 더 확인
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(WALLET_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Wallet data saved to {WALLET_DATA_FILE}")
        print(f"Saved wallet data: {data}")
    except Exception as e:
        print(f"Error saving wallet data: {e}")

# 데이터 초기화
try:
    registered_nfts = load_nfts()
    print(f"Loaded NFT data: {registered_nfts}")
    user_wallets = load_wallets()
    print(f"Loaded wallet data: {user_wallets}")
except Exception as e:
    print(f"Error loading data: {e}")
    registered_nfts = {}
    user_wallets = {}

# 샘플 NFT 이미지 목록 (실제로는 동적으로 로드하거나 DB에서 가져올 수 있음)
sample_nfts = [
    {"id": "nft001", "name": "DOVIARAE 아트픽셀001", "image": "images/nft1.png"},
    {"id": "nft002", "name": "DOVIARAE 아트픽셀002", "image": "images/nft2.png"},
    {"id": "nft003", "name": "DOVIARAE 아트픽셀003", "image": "images/nft3.png"},
    {"id": "4324325200111223", "name": "DOVIARAE 아트픽셀", "image": "images/4324325200111223.png"}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan')
def scan():
    return render_template('scan.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nft_id = request.form.get('nft_id')
        
        # 테스트를 위해 고정된 지갑 ID 사용
        wallet_id = TEST_WALLET_ID
        
        # 선택된 NFT 찾기
        selected_nft = next((nft for nft in sample_nfts if nft["id"] == nft_id), None)
        
        if selected_nft:
            # 사용자 지갑에 NFT 추가
            if wallet_id not in user_wallets:
                user_wallets[wallet_id] = []
            
            # NFT에 타임스킬프 추가
            nft_with_timestamp = selected_nft.copy()
            nft_with_timestamp["registered_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            user_wallets[wallet_id].append(nft_with_timestamp)
            # 고유번호 대신 NFT ID를 키로 사용
            registered_nfts[nft_id] = {"wallet_id": wallet_id, "nft_id": nft_id}
            
            # JSON 파일에 저장
            save_wallets(user_wallets)
            save_nfts(registered_nfts)
            
            return redirect(url_for('wallet', wallet_id=wallet_id))
    
    # GET 요청이거나 등록 실패 시
    nft_id = request.args.get('nft_id', '')
    return render_template('register.html', nft_id=nft_id)

@app.route('/success')
def success():
    wallet_id = request.args.get('wallet_id', '')
    if wallet_id in user_wallets:
        nfts = user_wallets[wallet_id]
        return render_template('success.html', wallet_id=wallet_id, nfts=nfts)
    return redirect(url_for('index'))

@app.route('/wallet/<wallet_id>')
def wallet(wallet_id):
    if wallet_id in user_wallets:
        nfts = user_wallets[wallet_id]
        return render_template('wallet.html', wallet_id=wallet_id, nfts=nfts)
    return redirect(url_for('index'))

@app.route('/API/reg/<nft_code>')
def api_register(nft_code):
    """외부 QR 코드에서 호출할 API 엔드포인트
    QR 코드에 이 URL을 포함시켜 스캔하면 register.html로 리디렉션됩니다.
    """
    # NFT 코드 검증 (실제로는 더 복잡한 검증 로직이 필요)
    # 여기서는 간단히 코드가 존재하는지만 확인
    if nft_code:
        # 코드에서 NFT ID 추출 (예: 첫 6자리)
        nft_id = f"nft{nft_code[:3]}"
        
        # 등록 페이지로 리디렉션
        return redirect(url_for('register', nft_id=nft_id))
    
    # 유효하지 않은 코드인 경우 메인 페이지로 리디렉션
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
