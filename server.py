# flask.py 안에 Flask class 로드
from flask import Flask
#요청관련 클래스
from flask import request
# html 로드하는 클래스 ~
from flask import render_template
# 파일 이름 경로에 대한 기본적인 보안
from werkzeug.utils import secure_filename

#flask server보안규칙
# 1. html 문서들은 render_template로 로드시
# 반드시 templates 폴더 내에 존재해야 한다.
# 2. 모든 경로에 대해 접근 불가
# 단, static 경로만 접근 가능

import os
# static/imgs 폴더가 없으면 만들어라
if not os.path.exists('static/imgs'):
    os.makedirs('static/imgs')




# 내장변수 __name__을 매개변수로 해서 Flask클래스 생성
# 생성된 인스턴스를 app에 저장
app = Flask(__name__)

# IPv4:port +'/' 경로로 접속시 호출되는 함수 정의
@app.route('/')
def index():

    # return에 HTML 사용한다.
        # 1.태그 직접 작성
        # 2. 라이브러리 사용 : render_template
    return """ 


    <h1>HTML 문서를 직접 만들자~</h1>
    
    <form action="/detect" method="post" enctype="multipart/form-data">
        <input type="file" name="file"> </br>
        <input type="submit" value="전송">
    </form>
    
    """

# root경로에서 넘어온 이미지를 받아오는 페이지
@app.route('/detect', methods=['POST'])
def detect():
    # request 관련 페이지들은 
    # route 설정 시 반드시 전송방식을 정의해야 한다
    
    # get 방식으로 던졌다면 : request.args['key값']
    # pors 방식으로 던졌다면 : request.form['key값']
    # file 방식으로 던졌다면 : request.files['key값']

    f = request.files['file']
    filename = secure_filename(f.filename)

    img_path = 'static/imgs/' + filename
    f.save(img_path)

    i = ImageDetect()
    result = i.detect_img(img_path)

    # 예외처리
    if result.size == 0:
        return "<h1>탐색결과 없음😣</h1>"
    
    cnf = result[0][4]
    numberClass = int(result[0][5])
    label = i.data[numberClass]

    #출력결과
    output = '<h1>{}일 확률이 {:.2f}%입니다.</h1>'.format(label, cnf * 100)
    return output
    
    
# 내가 직접 실행(run)시 내장 변수 __name__이 __main__으로 변한다.
if __name__ == '__main__':
    app.run(port=5088)
    