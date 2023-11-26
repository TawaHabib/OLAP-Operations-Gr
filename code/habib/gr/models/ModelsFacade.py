from models.GestureModels import Gesture
from models.HandModels import HandModel
from models.HandModels import HandProperty
from models.HandModels import HandSkeletalModel


def create_hand_model(hand_lm: list, property_hand: HandProperty) -> HandModel:
    return HandSkeletalModel(hand_lm, property_hand)


def create_gesture(hand_model: HandModel, gesture_id, gesture_name: str, score=0.8) -> Gesture:
    return Gesture(hand_model, gesture_name, gesture_id, score)


def create_hand_property(score: float, index: int, label: str) -> HandProperty:
    return HandProperty(score, index, label)


def get_hand_model_parameter(hand: HandModel) -> list:
    return hand.get_model_parameter()


def get_gesture_position(gesture: Gesture) -> [float, float]:
    return GestureFacade.get_hand_position(gesture.hand)


def get_hand_position(hand: HandModel) -> [float, float]:
    return hand.get_hand_position()


def get_gesture_name(gesture: Gesture) -> str:
    return gesture.gesture_name


def get_gesture_id(gesture: Gesture):
    return gesture.gesture_id


def get_hand_lm_list(hand: HandSkeletalModel) -> list[[float, float]]:
    return hand.get_hand_lm_list()


def get_hand_classification(hand: HandSkeletalModel):
    return hand.property_hand.index


def get_hand_name(hand: HandSkeletalModel):
    return hand.property_hand.label


def get_hand_property(hand: HandSkeletalModel) -> HandProperty:
    return hand.property_hand

