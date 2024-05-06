import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))
import requests
import cv2
import numpy as np
import json
from sdks.novavision.src.media.image import Image as image

from sdks.novavision.src.base.model import Image, Request
from capsules.capsule.src.utils.config import Config
from capsules.capsule.src.configs.config import CFG

from capsules.TrafficSignRecognition.src.models.PackageModel import PackageModel, PackageConfigs, ConfigExecutor, \
    TrafficSignRecognitionExecutor, TrafficSignRecognitionRequest, TrafficSignRecognitionInputs, InputImage, \
    TrafficSignRecognitionConfigs, DrawBBox, DrawBBoxEnable, DrawBBoxDisable

ENDPOINT_URL = "http://127.0.0.1:8000/api"


def inference():
    config = Config.from_json(CFG)
    # giriş görüntüsü base64 formatına dönüştürülüyor
    image_data = Image(name="image", uID="323332", mimeType="image/png", encoding="base64", value=image.encode64(
        np.asarray(cv2.imread(config.project.path + '/capsules/TrafficSignRecognition/resources/deneme.png')).astype(np.float32),
        'image/png'), type="Image")

    # drawBBoxDisable = DrawBBoxDisable(value="False")
    drawBBoxEnable = DrawBBoxEnable(value=True)
    drawBBox = DrawBBox(value= drawBBoxEnable)
    trafficSignRecognitionConfigs = TrafficSignRecognitionConfigs(drawBBox=drawBBox)
    inputImage = InputImage(value=image_data)
    trafficSignRecognitionInputs = TrafficSignRecognitionInputs(inputImage=inputImage)
    trafficSignRecognitionRequest = TrafficSignRecognitionRequest(inputs=trafficSignRecognitionInputs,
                                                                  configs=trafficSignRecognitionConfigs)
    trafficSignRecognitionExecutor = TrafficSignRecognitionExecutor(value=trafficSignRecognitionRequest)
    configExecutor = ConfigExecutor(value=trafficSignRecognitionExecutor)
    packageConfigs = PackageConfigs(executor=configExecutor)
    request = PackageModel(configs=packageConfigs, name="TrafficSignRecognition")
    request_json = json.loads(request.json())
    response = requests.post(ENDPOINT_URL, json=request_json)
    print(response.raise_for_status())
    print(response.json())



if __name__ =="__main__":
    inference()