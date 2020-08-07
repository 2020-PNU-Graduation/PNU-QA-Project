import tensorflow as tf
import numpy as np

# 학습 데이터 load
((train_data, train_label), (eval_data, eval_label)) = tf.keras.datasets.mnist.load_data()
# data를 정규화하여 28x28로 reshape
train_data = train_data / np.float32(255)
train_data = train_data.reshape(60000, 28, 28, 1)
train_data.shape
eval_data = eval_data / np.float32(255)
eval_data = eval_data.reshape(10000, 28, 28, 1)
eval_data.shape
from tensorflow.keras import models

# CNN으로 모델 생성
model = models.Sequential()
model.add(tf.keras.layers.Conv2D(32, (5, 5), padding='same', activation='relu', input_shape=(28, 28, 1)))
model.add(tf.keras.layers.MaxPooling2D((2, 2)))
model.add(tf.keras.layers.Conv2D(64, (5, 5), activation='relu'))
model.add(tf.keras.layers.MaxPooling2D((2, 2)))
model.add(tf.keras.layers.Conv2D(64, (5, 5), activation='relu'))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dense(10, activation='softmax'))
model.summary()
# graph를 생성하고 training
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(train_data, train_label, epochs=5)
test_loss, test_acc = model.evaluate(eval_data, eval_label, verbose=2)
test_acc
# save the model. TF 2.0에서는 experimental 대신 save_model만 하면됨
model_dir = "/tmp/tfkeras_mnist"
tf.keras.experimental.export_saved_model(model, model_dir)
