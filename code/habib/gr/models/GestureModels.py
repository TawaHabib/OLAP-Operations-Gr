from models.HandModels import HandModel


class Gesture(object):
    def __init__(self, hand: HandModel, gesture_name: str, gesture_id, score=0.8):
        self.hand: HandModel = hand
        self.gesture_name: str = gesture_name
        self.gesture_id = gesture_id
        self.score=score
