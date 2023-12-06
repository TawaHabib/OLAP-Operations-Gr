import importlib
import argparse
import time

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from threading import Thread

from models.GestureModels import Gesture
from util.ExecuterManager import ExecuteManager
from util.PrinterManager import Printer
from util.Util import Util


class Gesture_Executor(Thread):
    def update_gestures(self, gestures: list[Gesture]):
        pass

    def kill(self):
        pass


class Recognizer(Thread):
    encoding_file = 'utf-8'

    model_property_name = 'model_asset_path'
    num_hands_property_name = 'num_hands'
    min_hand_detection_confidence_property_name = 'min_hand_detection_confidence'
    min_hand_presence_confidence_property_name = 'min_hand_presence_confidence'
    min_tracking_confidence_property_name = 'min_tracking_confidence'

    def __init__(self, file_name: str, section_mediapipe_property_name: str, section_gesture_name: str,
                 executor: Gesture_Executor, to_print: bool = True, med_frame: int = 20):
        super().__init__()
        self.section_mediapipe_property_name = section_mediapipe_property_name
        self.section_gesture_name = section_gesture_name
        self.file_name = file_name
        self.life = True
        self.gesture_recognizer_result_list: list[Gesture] = []

        self.FPS = 0
        self.num_med_frame = med_frame
        self.start_time = time.time_ns()
        self.counter = 0
        self.executor = executor

        self.print = to_print

    def run(self):
        (model, num_hands, mhdc, mhpc,
         min_tracking_confidence) = (Util.get_mediapipe_gestures_recognizer_property(self.file_name,
                                                                                     self.section_mediapipe_property_name,
                                                                                     self.encoding_file))
        #copy reference
        gesture_recognizer_result_list: list[Gesture] = self.gesture_recognizer_result_list

        # Initialize the gesture recognizer model
        base_options = python.BaseOptions(model_asset_path=model)
        options = vision.GestureRecognizerOptions(base_options=base_options,
                                                  running_mode=vision.RunningMode.LIVE_STREAM,
                                                  num_hands=num_hands, min_hand_detection_confidence=mhdc,
                                                  min_hand_presence_confidence=mhpc, result_callback=self.save_result,
                                                  min_tracking_confidence=min_tracking_confidence)
        #create recognizer with some options
        recognizer = vision.GestureRecognizer.create_from_options(options)
        #
        cap = cv2.VideoCapture(0)
        printer = None

        if self.print:
            printer = Printer(cap, 'Output')

        self.executor.start()

        while self.life:
            # Read each frame from the webcam
            success, frame = cap.read()
            if not success:
                print('cant read frame')
                continue
            frame = cv2.flip(frame, 1)

            # convert in rgb frame
            framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # conversion in mp image del frame
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=framergb)
            try:
                recognizer.recognize_async(mp_image, time.time_ns() // 1_000_000)
            except Exception as e:
                print(e)

            if (printer is not None) and self.FPS > 0:
                printer.update(frame, gesture_recognizer_result_list, 'mp_FPS: '+str(self.FPS))
            elif printer is not None:
                printer.update(frame, gesture_recognizer_result_list)

            if (cv2.waitKey(1) == ord('q')
                    or (cv2.getWindowProperty("Output", cv2.WND_PROP_VISIBLE) < 1) and (printer is not None)):
                break

        recognizer.close()
        cap.release()
        cv2.destroyAllWindows()
        self.executor.kill()

    def save_result(self, result: mp.tasks.vision.GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):

        self.gesture_recognizer_result_list.clear()
        Util.save(result, self.gesture_recognizer_result_list)
        # print('model launching execute...')
        Util.update_gestures_names(gestures=self.gesture_recognizer_result_list,
                                   file_path=self.file_name, gesture_section=self.section_gesture_name, )
        self.executor.update_gestures(self.gesture_recognizer_result_list)

        if self.counter % self.num_med_frame == 0:
            self.FPS = int(self.num_med_frame/((time.time_ns()-self.start_time)/1000000000))
            self.start_time = time.time_ns()
        try:
            self.counter += 1
        except Exception as e:
            print(e)
            self.counter = 1
