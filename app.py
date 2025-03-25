from flask import Flask, request, jsonify, render_template, url_for, redirect, session
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
app.secret_key = 'your_key'

# 인증 정보 설정
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name("your_file.json", scope)
client = gspread.authorize(creds)
spreadsheet = client.open("test")

sheet1 = spreadsheet.get_worksheet(0)
sheet2 = spreadsheet.get_worksheet(1)

@app.route('/')
def index():

    records = sheet2.get_all_records()
    id_column=None

    count_options={
        "option1": 0,
        "option2": 0,
        "option3": 0,
        "option4": 0,
    }

    if records:  # records가 비어있지 않은 경우
        first_row = records[0]  # 첫 번째 행 가져오기
        id_column = [key for key in first_row.keys() if 'id' in key.lower()]
    
    for record in records:
            id_value = record.get(id_column[0])  # ID 열의 첫 번째 값 가져오기
            if id_value in count_options:  # 옵션 중 하나일 경우
                count_options[id_value] += 1  # 카운트 증가

    return render_template('index.html',count_options=count_options)  # index.html 렌더링

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    option1_users=[]
    option2_users=[]
    option3_users=[]
    option4_users=[]

    count_options={
        "option1": 0,
        "option2": 0,
        "option3": 0,
        "option4": 0,
        }
    
    records = sheet2.get_all_records()
    id_column=None
    row_to_update = None

    if records:  # records가 비어있지 않은 경우
        first_row = records[0]  # 첫 번째 행 가져오기
        id_column = [key for key in first_row.keys() if 'id' in key.lower()]
    
    for record in records:
            id_value = record.get(id_column[0])  # ID 열의 첫 번째 값 가져오기
            if id_value in count_options:  # 옵션 중 하나일 경우
                count_options[id_value] += 1  # 카운트 증가
            if id_value == 'option1' :
                term=record.get('기수')
                name=record.get('이름')
                if term and name:
                    option1_users.append({"term":term,"name":name})
            if id_value == 'option2' :
                term=record.get('기수')
                name=record.get('이름')
                if term and name:
                    option2_users.append({"term":term,"name":name})
            if id_value == 'option3' :
                term=record.get('기수')
                name=record.get('이름')
                if term and name:
                    option3_users.append({"term":term,"name":name})
            if id_value == 'option4' :
                term=record.get('기수')
                name=record.get('이름')
                if term and name:
                    option4_users.append({"term":term,"name":name})

    if request.method == 'POST':
        vote = request.form.get('vote') 
        vote_id = request.form.get('voteId')
        term = request.form.get('term')   
        name = request.form.get('name')   

        for i, record in enumerate(records):
            if record['이름'] == name and record['기수'] == term:  # 열 제목이 '이름'과 '기수'인 경우
                row_to_update = i + 2  # gspread의 인덱스는 1부터 시작하므로 +2
                break
        if row_to_update is not None:
            sheet2.update_cell(row_to_update, 5, vote_id)

        session['vote'] = vote
        session['term'] = term
        session['name'] = name

        if vote in ['참석']:  # '참석' 옵션 (option1, option2)에 해당
            return redirect(url_for('opinion'))  # /opinion 경로로 리다이렉트
        else:  # '불참' 옵션 (option3, option4)에 해당
            return redirect(url_for('end'))  # /end 경로로 리다이렉트

    return render_template('vote.html', count_options=count_options, option1_users=option1_users, option2_users=option2_users, option3_users=option3_users, option4_users=option4_users)

@app.route('/more1')
def more1():
    records = sheet2.get_all_records()
    id_column=None

    option1_users=[]

    count_options={
        "option1": 0,
        "option2": 0,
        "option3": 0,
        "option4": 0,
    }

    if records:  # records가 비어있지 않은 경우
        first_row = records[0]  # 첫 번째 행 가져오기
        id_column = [key for key in first_row.keys() if 'id' in key.lower()]
    
    for record in records:
            id_value = record.get(id_column[0])  # ID 열의 첫 번째 값 가져오기
            if id_value in count_options:  # 옵션 중 하나일 경우
                count_options[id_value] += 1  # 카운트 증가
            if id_value == 'option1' :
                term=record.get('기수')
                name=record.get('이름')
                if term and name:
                    option1_users.append({"term":term,"name":name})

    return render_template('more1.html',count_options=count_options, option1_users=option1_users) 

@app.route('/more2')
def more2():
    records = sheet2.get_all_records()
    id_column=None

    option2_users=[]

    count_options={
        "option1": 0,
        "option2": 0,
        "option3": 0,
        "option4": 0,
    }

    if records:  # records가 비어있지 않은 경우
        first_row = records[0]  # 첫 번째 행 가져오기
        id_column = [key for key in first_row.keys() if 'id' in key.lower()]
    
    for record in records:
            id_value = record.get(id_column[0])  # ID 열의 첫 번째 값 가져오기
            if id_value in count_options:  # 옵션 중 하나일 경우
                count_options[id_value] += 1  # 카운트 증가
            if id_value == 'option2' :
                term=record.get('기수')
                name=record.get('이름')
                if term and name:
                    option2_users.append({"term":term,"name":name})

    return render_template('more2.html',count_options=count_options, option2_users=option2_users) 

@app.route('/more3')
def more3():
    records = sheet2.get_all_records()
    id_column=None

    option3_users=[]

    count_options={
        "option1": 0,
        "option2": 0,
        "option3": 0,
        "option4": 0,
    }

    if records:  # records가 비어있지 않은 경우
        first_row = records[0]  # 첫 번째 행 가져오기
        id_column = [key for key in first_row.keys() if 'id' in key.lower()]
    
    for record in records:
            id_value = record.get(id_column[0])  # ID 열의 첫 번째 값 가져오기
            if id_value in count_options:  # 옵션 중 하나일 경우
                count_options[id_value] += 1  # 카운트 증가
            if id_value == 'option3' :
                term=record.get('기수')
                name=record.get('이름')
                if term and name:
                    option3_users.append({"term":term,"name":name})

    return render_template('more3.html',count_options=count_options, option3_users=option3_users) 

@app.route('/more4')
def more4():
    records = sheet2.get_all_records()
    id_column=None

    option4_users=[]

    count_options={
        "option1": 0,
        "option2": 0,
        "option3": 0,
        "option4": 0,
    }

    if records:  # records가 비어있지 않은 경우
        first_row = records[0]  # 첫 번째 행 가져오기
        id_column = [key for key in first_row.keys() if 'id' in key.lower()]
    
    for record in records:
            id_value = record.get(id_column[0])  # ID 열의 첫 번째 값 가져오기
            if id_value in count_options:  # 옵션 중 하나일 경우
                count_options[id_value] += 1  # 카운트 증가
            if id_value == 'option4' :
                term=record.get('기수')
                name=record.get('이름')
                if term and name:
                    option4_users.append({"term":term,"name":name})

    return render_template('more4.html',count_options=count_options, option4_users=option4_users) 


@app.route('/opinion', methods=['GET', 'POST'])
def opinion():
    if request.method == 'POST':
        vote1=request.form.get('vote1')
        vote2=request.form.get('vote2')

        vote = session.get('vote')
        term = session.get('term')
        name = session.get('name')

        records = sheet1.get_all_records()
        row_to_update = None
       
        # 기수와 이름이 일치하는 행 찾기
        for i, record in enumerate(records):
            if record['이름'] == name and record['기수'] == term:  # 열 제목이 '이름'과 '기수'인 경우
                row_to_update = i + 2  # gspread의 인덱스는 1부터 시작하므로 +2
                break
        if row_to_update is not None:
            sheet1.update_cell(row_to_update, 5, vote)
            sheet1.update_cell(row_to_update, 6, vote1)
            sheet1.update_cell(row_to_update, 7, vote2)

        return redirect(url_for('end'))


    return render_template('opinion.html')  # GET 요청 시 HTML 페이지 반환

@app.route ('/end')
def end():
    return render_template('end.html')

if __name__ == '__main__':
    app.run(debug=True)
