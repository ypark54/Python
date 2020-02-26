import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

data = keras.datasets.fashion_mnist

gpus = tf.config.experimental.list_physical_devices('GPU')

if gpus:
  try:
    tf.config.experimental.set_memory_growth(gpus[0], True)
  except RuntimeError as e:
    print(e)

(train_images, train_labels), (test_images, test_labels) = data.load_data()
print(len(train_images[0][0]))
# Normalize the images.
train_images = (train_images / 255) - 0.5
test_images = (test_images / 255) - 0.5

# Reshape the images.
train_images = np.expand_dims(train_images, axis=3)
test_images = np.expand_dims(test_images, axis=3)

num_filters = 16
filter_size = 3
pool_size = 2

# Build the model.
model = keras.models.Sequential([
  keras.layers.Conv2D(num_filters, filter_size, input_shape=(28, 28, 1)),
  keras.layers.MaxPooling2D(pool_size=pool_size),
  keras.layers.Flatten(),
  keras.layers.Dense(256, activation = "relu"),
  keras.layers.Dense(256, activation = "relu"),
  keras.layers.Dense(256, activation = "relu"),
  keras.layers.Dropout(0.2),
  keras.layers.Dense(10, activation='softmax'),
])

# Compile the model.
model.compile(optimizer="adam", loss = "sparse_categorical_crossentropy", metrics=["accuracy"])
# Train the model.
model.fit(train_images, train_labels, epochs=5)
test_loss, test_acc = model.evaluate(test_images, test_labels)
print(test_acc)