import tensorflow as tf
import numpy as np

# eval data 불러오고
((train_data, train_label), (eval_data, eval_label)) = tf.keras.datasets.mnist.load_data()
eval_data = eval_data / np.float32(255)
eval_data = eval_data.reshape(10000, 28, 28, 1)
# 저장한 모델 불러 온뒤
model_dir = "/tmp/tfkeras_mnist"
new_model = tf.keras.experimental.load_from_saved_model(model_dir)
new_model.summary()
# 그래프를 형성하고,
new_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
# 임의의 위치에 있는 MNIST 숫자를 하나 읽어서 예측
random_idx = np.random.choice(eval_data.shape[0])
test_data = eval_data[random_idx].reshape(1, 28, 28, 1)
res = new_model.predict(test_data)
# 제대로 학습되었는지 확인
print("predict: {}, original: {}".format(np.argmax(res), eval_label[random_idx]))
