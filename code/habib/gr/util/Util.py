import configparser
import win32com.client
import cv2
import mediapipe as mp
from mediapipe.tasks.python.vision import GestureRecognizerResult

from models import ModelsFacade
from models.GestureModels import Gesture


class Util:

    @staticmethod
    def save(gesture_recognizer_result: GestureRecognizerResult, gesture_list: list[Gesture]):
        gesture = 0
        for hand_landmarks in gesture_recognizer_result.hand_landmarks:
            try:
                gesture_list.append(
                    ModelsFacade.create_gesture(
                        ModelsFacade.create_hand_model(
                            hand_landmarks,
                            ModelsFacade.create_hand_property(
                                gesture_recognizer_result.handedness[gesture][0].score,
                                gesture_recognizer_result.handedness[gesture][0].index,
                                gesture_recognizer_result.handedness[gesture][0].category_name
                            )
                        ),
                        gesture_recognizer_result.gestures[gesture][0].category_name,
                         'ndn', gesture_recognizer_result.gestures[gesture][0].score
                    )
                )
                gesture += 1
            except Exception as e:
                print(e)

    @staticmethod
    def if_not_in_range_get_default(value, minimum, maximum, default):
        ret = default
        if value >= minimum or value <= maximum:
            ret = value

        return ret

    @staticmethod
    def get_properties_from_file(filename: str, encoding: str, section: str, prop: str) -> str:
        cfg = configparser.RawConfigParser()
        try:
            cfg.read(filename, encoding)
        except Exception as e:
            print(e)
        try:
            return cfg.get(section, prop)
        except Exception as e:
            print(e)
            return '0'

    @staticmethod
    def print_hand_connections(gestures: list[Gesture], frame):
        for g in gestures:
            mp.solutions.drawing_utils.draw_landmarks(frame, g.hand.get_model_parameter(),
                                                      mp.solutions.hands.HAND_CONNECTIONS,
                                                      mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
                                                      mp.solutions.drawing_styles.get_default_hand_connections_style())

    @staticmethod
    def print_on_frame(text_to_print: str, frame, gesture_position: [int, int], color):
        cv2.putText(
            frame,
            text_to_print,
            gesture_position,
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            color,
            2,
            cv2.LINE_AA
        )

    @staticmethod
    def get_mediapipe_gestures_recognizer_property(file_name: str,
                                                   section_mediapipe_property_name: str,
                                                   encoding_file: str):

        model_property_name = 'model_asset_path'
        num_hands_property_name = 'num_hands'
        min_hand_detection_confidence_property_name = 'min_hand_detection_confidence'
        min_hand_presence_confidence_property_name = 'min_hand_presence_confidence'
        min_tracking_confidence_property_name = 'min_tracking_confidence'
        model = str(Util.get_properties_from_file(file_name, encoding_file,
                                                  section_mediapipe_property_name, model_property_name))

        num_hands = Util.if_not_in_range_get_default(
            int(Util.get_properties_from_file(file_name, encoding_file,
                                              section_mediapipe_property_name, num_hands_property_name)),
            1, 10, 1)

        min_hand_detection_confidence = Util.if_not_in_range_get_default(
            float(Util.get_properties_from_file(file_name, encoding_file, section_mediapipe_property_name,
                                                min_hand_detection_confidence_property_name)),
            0, 1, 0.5)

        min_hand_presence_confidence = Util.if_not_in_range_get_default(
            float(Util.get_properties_from_file(file_name, encoding_file, section_mediapipe_property_name,
                                                min_hand_presence_confidence_property_name)),
            0, 1, 0.5)

        min_tracking_confidence = Util.if_not_in_range_get_default(
            float(Util.get_properties_from_file(file_name, encoding_file, section_mediapipe_property_name,
                                                min_tracking_confidence_property_name)),
            0, 1, 0.5)
        return model, num_hands, min_hand_detection_confidence, min_hand_presence_confidence, min_tracking_confidence

    @staticmethod
    def update_gestures_names(gestures: list[Gesture], file_path: str, gesture_section: str):
        for g in gestures:
            g.gesture_name = Util.get_properties_from_file(filename=file_path, section=gesture_section,
                                                           encoding='utf-8', prop=g.gesture_id)


class Color:
    red = (0, 0, 255)
    blu = (255, 0, 0)
    green = (0, 255, 0)
    white = (255, 255, 255)
    black = (0, 0, 0)


class Ppt:
    #app = win32com.client.Dispatch("PowerPoint.Application")

    def __init__(self, path_to_file: str, app=win32com.client.Dispatch("PowerPoint.Application")):
        self.app = app
        self.presentation_mode: bool = False
        self.file_name = path_to_file
        self.objCOM = app.Presentations.Open(FileName=path_to_file, WithWindow=1)
        self.current_slide = 1

    def active_presentation_mode(self):
        self.objCOM.SlideShowSettings.Run()
        self.objCOM.SlideShowWindow.Activate()
        self.presentation_mode = True

    def next(self):
        self.check_presentation_mode()
        self.current_slide += 1
        try:
            self.objCOM.SlideShowWindow.View.GotoSlide(self.current_slide)
        except Exception as e:
            print('ERROR: '+str(e))
            self.current_slide -= 1

    def previous(self):
        self.check_presentation_mode()
        self.current_slide -= 1
        try:
            self.objCOM.SlideShowWindow.View.GotoSlide(self.current_slide)
        except Exception as e:
            print('ERROR: '+str(e))
            self.current_slide += 1

    def close(self):
        self.objCOM.Close()

    def check_presentation_mode(self):
        if not self.presentation_mode:
            self.active_presentation_mode()

    def quit(self):
        self.app.Quit()
