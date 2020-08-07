from flask import Flask , render_template, request
import time

app = Flask(__name__)


@app.route('/')
def index():
    title = "이것은 타이틀이다."
    return render_template('tableView.html', title=title)

@app.route('/getTableData', methods=['POST'])
def getTableAndShow():
    value = request.form['tableData']
    return render_template('tableView.html', table='선택한 테이블 보여주기')


@app.route('/postQuestion', methods=['POST'])
def postQuestion():
    value = request.form['test']
    question = value
    answer = prediction(question)
    return render_template('tableView.html', question=question, answer=answer)


def prediction(question):
    time.sleep(3)
    answer = '예시 정답 텍스트'
    return answer


if __name__ == '__main__':
    app.run(debug = True)


