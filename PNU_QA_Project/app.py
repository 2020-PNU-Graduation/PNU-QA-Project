from flask import Flask , render_template, request

app = Flask(__name__)


@app.route('/')
def index():

    return render_template('tableView.html')

@app.route('/handle_data',methods = ['POST'])
def handle_data():
    projectpath = request.form['table']
    print(projectpath)
    return projectpath

@app.route('/post', methods=['POST'])
def post():
    value = request.form['test']
    print(value)
    return value


if __name__ == '__main__':
    app.run(debug = True)


# 오후 5:36 조상현 전에 설명드렸던 내용중에
# 오후 5:36 조상현 대/소 관계 구분을 위해서
# 오후 5:36 조상현 별도로 처리가 필요하다고 말씀드렸었는데
# 오후 5:36 조상현 그부분을 위해서 구현할 구현해주셔야 될 부분이 있습니다
# 오후 5:36 조상현 우선 테이블은 행/열이 있는데
# 오후 5:37 조상현 이걸 저희가 사용하는 시스템에서 표현할 때에는
# 오후 5:37 조상현 예를 들어 테이블 헤드가 "이름, 나이"라면
# 오후 5:38 조상현 ['홍길동', '25']의 리스트를 행의 개수만큼 담고있는 리스트가 테이블 데이터가 됩니다
# 오후 5:38 조상현 [ ['홍길동, '25'], ['김철수, '26'], ['김영희', '27'] ]
# 오후 5:39 조상현 행3, 열2의 테이블 데이터를 표현하는 데이터가 됩니다
# 오후 5:40 조상현 해당 데이터 형식에서 대/소 관계 구분을 위해서 숫자 데이터에 대한 순위 정보를 표현하는 배열을 생성하는 함수를 구현해주셔야 합니다
# 오후 5:40 조상현 위의 예시 테이블에서 순위 배열을 생성하면
# 오후 5:40 조상현 이름이라는 데이터는 텍스트니까 순위를 표현못하기 때문에 무조건 0으로 고정하게 되고
# 오후 5:41 조상현 [ [0, 0], [0, 1], [0, 2] ]의
# 오후 5:41 조상현 배열을 생성시켜주시면 됩니다
