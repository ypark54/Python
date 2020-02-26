import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

data = keras.datasets.fashion_mnist

(train_images, train_labels), (test_images, test_labels) = data.load_data()

#plt.imshow(train_images[0])
#print(train_labels[0])
#plt.show()

train_images_scale_down = train_images/256
test_images_scale_down = test_images/256

#train_images_scale_down = np.expand_dims(train_images_scale_down, axis=3)
#test_images_scale_down = np.expand_dims(test_images_scale_down, axis=3)


#print(train_images_scale_down[0])

model = keras.Sequential([
    #keras.layers.Conv2D(8,3,input_shape = (28,28, 1)),
    #keras.layers.MaxPooling2D(pool_size=2),
    keras.layers.Flatten(input_shape = (28,28)),
    keras.layers.Dense(128, activation = "relu"),
    keras.layers.Dense(128, activation = "relu"),
    keras.layers.Dense(128, activation = "relu"),
    keras.layers.Dense(10, activation = "softmax")
])

model.compile(optimizer="adam", loss = "sparse_categorical_crossentropy", metrics=["accuracy"])
#for x in range(5):
model.fit(train_images_scale_down, train_labels, epochs=5)
    #train_loss, train_acc = model.evaluate(train_images_scale_down, train_labels)
test_loss, test_acc = model.evaluate(test_images_scale_down, test_labels)
print(test_acc)
    #prediction_array = model.predict(test_images_scale_down)
    #prediction = [list(p).index(max(p)) for p in list(prediction_array)]

    #count_True = 0
    #count_False = 0
    #for x, y in zip(prediction, list(test_labels)):
    #    if x == y:
    #        count_True += 1
    #    else:
    #        count_False += 1

    #print(count_True, count_False)




if __name__ == '__main__':
    print("Hello World")