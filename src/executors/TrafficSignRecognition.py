import numpy as np
import sys
import os
import cv2

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from capsules.TrafficSignRecognition.src.utils.config import Config
from capsules.TrafficSignRecognition.src.configs.config import CFG
from sdks.novavision.src.media.image import Image as ImageSrc
from capsules.TrafficSignRecognition.src.models.PackageModel import TrafficSignRecognitionOutputs, PackageModel, \
    PackageConfigs, Image, ConfigExecutor, TrafficSignRecognitionResponse, TrafficSignRecognitionExecutor, OutputImage, \
    OutputDetection, Detection
from sdks.novavision.src.base.response import Response
from sdks.novavision.src.base.capsule import Capsule
from keras.models import load_model
import json


class TrafficSignRecognition(Capsule):
    def __init__(self, request, bootstrap):
        self.error_list = []

        super().__init__(request)
        self.config = Config.from_json(CFG)
        self.model = bootstrap["model"]
        self.request.model = PackageModel(**(self.request.data))
        self.inputImage = self.request.get_param("inputImage")
        self.is_list = False
        self.drawBBox = self.request.get_param("DrawBBox")

    @staticmethod
    def bootstrap():
        config = Config.from_json(CFG)
        saved_path = config.project.path + '/capsules/TrafficSignRecognition/src/weights/Trafic_signs_model.h5'
        model = load_model(saved_path)
        model = {"model": model}
        return model

    def infer(self, image):
        config = Config.from_json(CFG)
        image = np.expand_dims(image, axis=0)
        image = np.array(image)
        with open(config.project.path+'/capsules/TrafficSignRecognition/src/classes/classes.json', 'r') as f:
            classes = json.load(f)
        json.dumps(classes)
        pred_probabilities = self.model.predict(image)[0]
        pred_class = np.argmax(pred_probabilities)
        pred_label = classes[str(pred_class + 1)]

        return pred_label, pred_probabilities[pred_class]

    def run(self):
        pred_list = []
        if (self.is_list):
            for img_data in self.inputImage:
                img = ImageSrc.get_image(img_data)
                img_value = ImageSrc.encode64(img.value, "image/png")
                img_value = ImageSrc.decode64(img_value)
                resized_img = cv2.resize(img_value, (30, 30))
                pred = self.infer(resized_img)
                pred_encoded = ImageSrc.encode64(img_value, img.mimeType)
                pred_list.append(pred_encoded)
        else:
            img = ImageSrc.get_image(self.inputImage)
            img_value = ImageSrc.encode64(img.value, "image/png")
            img_value = ImageSrc.decode64(img_value)
            resized_img = cv2.resize(img_value, (30, 30))
            label, confidence = self.infer(resized_img)
            pred_encoded = ImageSrc.encode64(img_value, img.mimeType)
            img.value = pred_encoded
            pred_list.append(pred_encoded)
            detect_list = [Detection(
                confidence=confidence,
                detectedLabel=label,
            )]

        outputImage = OutputImage(value=img)
        outputDetection = OutputDetection(value=detect_list)
        trafficSignRecognitionOutputs = TrafficSignRecognitionOutputs(outputImage=outputImage,
                                                                      outputDetection=outputDetection)
        trafficSignRecognitionResponse = TrafficSignRecognitionResponse(outputs=trafficSignRecognitionOutputs)
        trafficSignRecognitionExecutor = TrafficSignRecognitionExecutor(value=trafficSignRecognitionResponse)
        executor = ConfigExecutor(value=trafficSignRecognitionExecutor)
        packageConfigs = PackageConfigs(executor=executor)
        packageModel = PackageModel(configs=packageConfigs)
        return Response(model=packageModel).response()
