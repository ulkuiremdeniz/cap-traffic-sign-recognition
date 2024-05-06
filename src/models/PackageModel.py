import numbers

from pydantic import Field, validator
from typing import List, Optional, Union, Any, Dict,Literal

from sdks.novavision.src.base.model import Package,Input, Output, Image, Config, Inputs, Configs, Outputs, Response, Request, Detection


class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image],Image]
    type = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Images"

class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image],Image]
    type = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Images"


class OutputDetection(Output):
    name: Literal["outputDetections"] = "outputDetections"
    value: List[Detection]
    type: Literal["list"] = "list"

    class Config:
        title = "Detections"


class DrawBBoxEnable(Config):
    name: Literal["drawBBoxEnable"] = "drawBBoxEnable"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
     title = "Enable"


class DrawBBoxDisable(Config):
    name: Literal["DrawBBoxDisable"] = "DrawBBoxDisable"
    value: Literal[False] = False
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Disable"


class DrawBBox(Config):
    name: Literal["DrawBBox"] = "DrawBBox"
    value: Union[DrawBBoxEnable,DrawBBoxDisable]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "DrawBBox"



class TrafficSignRecognitionInputs(Inputs):
    inputImage: InputImage



class TrafficSignRecognitionConfigs(Configs):
   drawBBox: DrawBBox



#paketin outputlarının birleştiği yer
class TrafficSignRecognitionOutputs(Outputs):
   #outputları class olarak tanımlaman gerekli
   outputImage:OutputImage
   outputDetection:OutputDetection




class TrafficSignRecognitionRequest(Request):
    inputs :Optional[TrafficSignRecognitionInputs]
    #config yanda verilen seçenek yeri kullanıcının girdiği parametre
    configs: TrafficSignRecognitionConfigs

    class Config:
        schema_extra = {
            "target": "configs"
        }


class TrafficSignRecognitionResponse(Response):
    outputs: TrafficSignRecognitionOutputs


# configexecutor de tanımladığın her executerın bir classı vardır
class TrafficSignRecognitionExecutor(Config):
    name: Literal["TrafficSignRecognition"] = "TrafficSignRecognition"

    #executerın request ve responselarını value değerine veriyoruz
    #value neyse type odur
    value: Union[TrafficSignRecognitionRequest, TrafficSignRecognitionResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        #kullanıcı tarafında executerın webde  görünen isimi
        title = "Traffic Sign Recognition"
        schema_extra = {
            "target": {
                "value": 0
            }
        }



class ConfigExecutor(Config):
    #executer klasöründe bu classa ulaşmamızı sağlayan isim
    name: Literal["ConfigExecutor"] = "ConfigExecutor"

    #birden fazla executor varsa bu şekilde belirtiyoruz
    #value: Union[Executor1,Executor2]
    #union:value değeri birden fazla değer alabilir
    value: Union[TrafficSignRecognitionExecutor]

    #value değerinin tipi
    #literal type değişmez başka bir şey veremezsin(final gibi)
    type:Literal["executor"] = "executor"

    #bu classın web tarafındaki kullanıcıya sunulan input taraflarının backend kısmı gibi...
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"

        #eğer birden fazla varsa kullanma
        #eğer 1 tane executor varsa target değeri value olarak verilecek
        schema_extra = {
           "target":"value"
        }


#executorlar packagemodel'e buradan bağlantı yapıyor
class PackageConfigs(Configs):
    executor: ConfigExecutor


#1.paketin özelliklerini belirtiyoruz
class PackageModel(Package):
    configs: PackageConfigs
    #paketin tipine göre belirliyoruz(capsules,components,widgets)
    type: Literal["TrafficSignRecognition"] = "TrafficSignRecognition"
    #paketin adı
    name: Literal["TrafficSignRecognition"] = "TrafficSignRecognition"
    uID = "1221112"