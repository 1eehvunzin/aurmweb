import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 인증 정보 설정
scope = [
    "https://www.googleapis.com/auth/spreadsheets",  # 구글 스프레드시트 읽기 및 쓰기 권한
    "https://www.googleapis.com/auth/drive"          # 구글 드라이브 접근 권한
    ]
creds = ServiceAccountCredentials.from_json_keyfile_name("midyear-system-322103-755e03135276.json", scope)
client = gspread.authorize(creds)

# 스프레드시트 열기
spreadsheet = client.open("test")
sheet = spreadsheet.sheet1  # 첫 번째 시트를 선택

# 웹 폼에서 받은 데이터를 예로 추가 (이곳에 실제 폼 데이터를 입력)
attendance = "테스트"  # 예: 참석 여부
opinion = "찬성"  # 예: 입장

# 데이터를 스프레드시트에 추가
sheet.append_row([attendance, opinion])

print("데이터가 성공적으로 추가되었습니다.")
