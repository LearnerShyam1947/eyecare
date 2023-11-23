from keras.preprocessing import image
from keras.models import load_model
from PIL import Image, ImageOps
import tensorflow as tf
import numpy as np

class_names=['cataract','diabetic_retinopathy','glaucoma','normal']

def predict_disease(img_path, model_path, class_names=class_names):
    model = load_model(model_path, compile=False)
    model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

    img = image.load_img(img_path,target_size = (224,224)) 
    
    x = image.img_to_array(img) 
    x = np.expand_dims(x,axis = 0)
    
    prediction = model.predict(x)
    pred = np.argmax(prediction,axis = 1)
    
    disease = str(class_names[pred[0]])
    confidence_score = max(prediction[0][pred])
    
    print("Predicted result : ",disease)
    print("Confidence Score : ",confidence_score)

    result = {
        'disease' : disease,
        'score' : confidence_score
    }

    return result

def prepare_image(image, image_size):
    image = tf.image.decode_jpeg(image, channels=3)

    image = tf.cast(image, tf.float32)
    image /= 255.0
    image = tf.image.resize(image, [image_size, image_size])

    image = np.expand_dims(image, axis=0)

    return image

def classify_using_bytes(image_bytes, model_path, image_size=224):
    model = load_model(model_path, compile=False)
    model.compile(
            loss='categorical_crossentropy',
            optimizer='adam',
            metrics=['accuracy']
        )

    prediction = model.predict(prepare_image(image_bytes, image_size))
    index = np.argmax(prediction, axis=1)[0]

    class_name = class_names[index]
    confidence_score = prediction[0][index]

    return {
        'class' : class_name,
        'score' : f'{confidence_score*100:02.2f}%'
    }

def predict_class(filepath, model_path, image_size = 224):
    np.set_printoptions(suppress=True)

    model = load_model(model_path ,compile=False)
    model.compile(
        loss='categorical_crossentropy',
        optimizer='adam',
        metrics=['accuracy']
    )

    data = np.ndarray(shape=(1, image_size, image_size, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(filepath).convert("RGB")

    # resizing the image to be at least 299 X 299 and then cropping from the center
    size = (image_size, image_size)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    # print("Class:", class_name[2:], end=" \n")
    # print("Confidence Score:", confidence_score)

    result = {
        "class" : class_name,
        "score" :f'{(confidence_score*100):2.2f}%'
    }

    return result

if __name__ == "__main__":
    print(predict_class("Diabetic Retinopathy.jpg", "models/model.h5"))

