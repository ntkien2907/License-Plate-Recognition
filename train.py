from config import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications import InceptionResNetV2
from tensorflow.keras.layers import Dense, Flatten, Input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.callbacks import EarlyStopping


df = pd.read_csv(LABELS_CSV)

# Read data
labels = df.iloc[:, 1:].values
data   = []
output = []
img_paths = list(df['filepath'])

for img_path, label in zip(img_paths, labels):
    img_arr = cv2.imread(img_path)
    h, w, d = img_arr.shape

    load_image = load_img(img_path, target_size=(224,224))
    load_image_arr = img_to_array(load_image)
    norm_load_image_arr = load_image_arr / 255.0

    xmin, xmax, ymin, ymax = label
    nxmin, nxmax = xmin / w, xmax / w
    nymin, nymax = ymin / h, ymax / h
    label_norm = (nxmin, nxmax, nymin, nymax)
    
    data.append(norm_load_image_arr)
    output.append(label_norm)


# Split train and test set
X = np.array(data, dtype=np.float32)
y = np.array(output, dtype=np.float32)
X, y = shuffle(X, y, random_state=RANDOM_STATE)
x_train, x_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=RANDOM_STATE)

# Build model
inception_resnet = InceptionResNetV2(weights="imagenet", include_top=False, input_tensor=Input(shape=(224,224,3)))
headmodel = inception_resnet.output
headmodel = Flatten()(headmodel)
headmodel = Dense(500, activation="relu")(headmodel)
headmodel = Dense(250, activation="relu")(headmodel)
headmodel = Dense(4, activation='sigmoid')(headmodel)
model = Model(inputs=inception_resnet.input, outputs=headmodel)
model.compile(loss='mse', optimizer=Adam(learning_rate=1e-4))

# Train and save
early_stopping = EarlyStopping(monitor='val_loss', patience=5, mode='min')
history = model.fit(x=x_train, 
                    y=y_train, 
                    batch_size=BATCH_SIZE, 
                    epochs=N_EPOCHS, 
                    validation_data=(x_test, y_test), 
                    callbacks=[early_stopping])

# Save model
model.save(MODEL)

# Summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['train', 'test'], loc='upper right')
plt.savefig(LOSS_JPG)