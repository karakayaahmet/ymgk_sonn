from django.db import models
from django.conf import settings
from PIL import Image
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
from tensorflow.python import ops
from keras.models import load_model
import os
import numpy as np
import tensorflow as tf


class Resimler(models.Model):
    image = models.ImageField(upload_to='media/')
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    average_color = models.TextField()

    class Meta:
        get_latest_by = 'created_at'

    def save(self, *args, **kwargs):
        # Open the image file
        with Image.open(self.image) as img:
            # Get the average color of the image
            average_color = img.getcolors(img.size[0]*img.size[1])
            # convert the color tuple to string to save it in the model
            average_color = str(average_color)
            # save the color in the model
            self.average_color = average_color
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        img = Image.open(self.image)
        test_img = img.resize((224, 224))
        test_img = img_to_array(test_img)
        test_img = np.expand_dims(test_img, axis=0)

        classes_tur = ["AageanRose", "AfyonBal", "AfyonBeyaz", "AfyonBlack", "AfyonGrey", "AfyonSeker", "Bejmermer",
                       "Blue", "Capuchino", "Diyabaz", "DolceVita", "EkvatorPijama", "ElazigVisne", "GoldGalaxy",
                       "GulKurusu", "KaplanPostu", "Karacabeysiyah", "Konglomera", "KristalEmprador", "Leylakmermer",
                       "MediBlack", "OliviaMarble", "Oniks", "RainGrey", "Traverten"]

        try:
            interpreter = tf.lite.Interpreter(model_path="yeni-tur_model.tflite")
            interpreter.allocate_tensors()
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()

            input_shape = input_details[0]['shape']
            interpreter.set_tensor(input_details[0]['index'], test_img)
            interpreter.invoke()

            output_data = interpreter.get_tensor(output_details[0]['index'])
            output_probs = tf.math.softmax(output_data)
            pred_label = tf.math.argmax(output_probs)

            predictions = output_probs
            print(predictions)

            max_index = np.argmax(predictions)
            classes = ["AageanRose", "AfyonBal", "AfyonBeyaz", "AfyonBlack", "AfyonGrey", "AfyonSeker", "Bejmermer",
                       "Blue", "Capuchino", "Diyabaz", "DolceVita", "EkvatorPijama", "ElazigVisne", "GoldGalaxy",
                       "GulKurusu", "KaplanPostu", "Karacabeysiyah", "Konglomera", "KristalEmprador", "Leylakmermer",
                       "MediBlack", "OliviaMarble", "Oniks", "RainGrey", "Traverten"]
            print(max_index)
            print(classes[max_index])
            self.title = str(classes[max_index])
            # file_model = os.path.join(settings.BASE_DIR, "yeni-tur_model.h5")
            # graph = tf.compat.v1.get_default_graph()
            #
            # with graph.as_default():
            #     model = load_model(file_model)
            #     pred = np.argmax(model.predict(test_img))
            #     self.title = str(classes_tur[pred])

        except:
            self.title = "sınıflandırma başarısız"

        return super().save(*args, **kwargs)






