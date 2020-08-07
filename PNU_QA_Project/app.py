from flask import Flask, render_template, request
import time
import numpy as np
import tensorflow as tf



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
    # 데이터를 읽어들이고
    ((train_data, train_label), (eval_data, eval_label)) = tf.keras.datasets.mnist.load_data()
    eval_data = eval_data / np.float32(255)
    eval_data = eval_data.reshape(10000, 28, 28, 1)
    # 저장해 두었던 모델을 읽어들인 후
    model_dir = "/tmp/tfkeras_mnist"
    new_model = tf.keras.experimental.load_from_saved_model(model_dir)
    new_model.summary()
    # 그래프를 생성하고
    new_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    answer = '예시 정답 텍스트'
    random_idx = np.random.choice(eval_data.shape[0])
    test_data = eval_data[random_idx].reshape(1, 28, 28, 1)
    res = new_model.predict(test_data)
    answer = "predict: {}, original: {}".format(np.argmax(res), eval_label[random_idx])
    print(answer)
    return answer


if __name__ == '__main__':
    app.run(debug=True)
