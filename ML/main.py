import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import Image
from sklearn.metrics import confusion_matrix
import time
from datetime import timedelta
import math

data = keras.datasets.fashion_mnist

(train_images, train_labels), (test_images, test_labels) = data.load_data()


# Normalize the images.
train_images = (train_images / 255) - 0.5
test_images = (test_images / 255) - 0.5

# Reshape the images.
train_images = np.expand_dims(train_images, axis=3)
test_images = np.expand_dims(test_images, axis=3)

num_filters = 8
filter_size = 3
pool_size = 2

# Build the model.
model = keras.models.Sequential([
  keras.layers.Conv2D(num_filters, filter_size, input_shape=(28, 28, 1)),
  keras.layers.MaxPooling2D(pool_size=pool_size),
  keras.layers.Flatten(),
  keras.layers.Dense(128, activation = "relu"),
  keras.layers.Dense(10, activation='softmax'),
])

# Compile the model.
model.compile(optimizer="adam", loss = "sparse_categorical_crossentropy", metrics=["accuracy"])
# Train the model.
model.fit(train_images, train_labels, epochs=5)
test_loss, test_acc = model.evaluate(test_images, test_labels)
print(test_acc)