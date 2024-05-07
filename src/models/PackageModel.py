
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




class TrafficSignRecognitionOutputs(Outputs):
   outputImage:OutputImage
   outputDetection:OutputDetection




class TrafficSignRecognitionRequest(Request):
    inputs :Optional[TrafficSignRecognitionInputs]
    configs: TrafficSignRecognitionConfigs

    class Config:
        schema_extra = {
            "target": "configs"
        }


class TrafficSignRecognitionResponse(Response):
    outputs: TrafficSignRecognitionOutputs


class TrafficSignRecognitionExecutor(Config):
    name: Literal["TrafficSignRecognition"] = "TrafficSignRecognition"
    value: Union[TrafficSignRecognitionRequest, TrafficSignRecognitionResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Traffic Sign Recognition"
        schema_extra = {
            "target": {
                "value": 0
            }
        }



class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[TrafficSignRecognitionExecutor]
    type:Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"

        schema_extra = {
           "target":"value"
        }



class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["TrafficSignRecognition"] = "TrafficSignRecognition"
    name: Literal["TrafficSignRecognition"] = "TrafficSignRecognition"
    uID = "1221112"