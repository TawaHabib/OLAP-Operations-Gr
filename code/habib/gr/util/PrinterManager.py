import cv2
import mediapipe as mp
import models.ModelsFacade as Mf
import numpy

from util.Util import Color
from util.Util import Util


class Printer:
    def __init__(self, cap: cv2.VideoCapture, frame_name: str, frame: numpy.ndarray = None,
                 gestures: list[Mf.Gesture] = None):
        self.gestures = gestures
        self.cap = cap
        self.frameName = frame_name
        self.frame = frame
        self.x, self.y, self.c = 0, 0, 0

    def update_gestures(self, gestures: list[Mf.Gesture]):
        self.gestures = gestures
        self.print()

    def update(self, frame: numpy.ndarray, gestures: list[Mf.Gesture], FPS = ''):
        self.x, self.y, self.c = frame.shape
        self.frame = frame
        self.gestures = gestures
        Util.print_on_frame(FPS, self.frame, [25, 25],Color.red)
        self.print()
        return self.frame

    def print(self):

        for g in self.gestures:
            mp.solutions.drawing_utils.draw_landmarks(self.frame, g.hand.get_model_parameter(),
                                                      mp.solutions.hands.HAND_CONNECTIONS,
                                                      mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
                                                      mp.solutions.drawing_styles.get_default_hand_connections_style())

            gesture_position = [int(g.hand.get_hand_position().pop(0) * self.y),
                                int(g.hand.get_hand_position().pop(1) * self.x)]
            Util.print_on_frame(g.gesture_name, self.frame, gesture_position, Color.red)

        # show frame
        cv2.imshow(self.frameName, self.frame)

    def print_string(self, string: str, position, color=Color.red):
        Util.print_on_frame(string, self.frame, position, color)

