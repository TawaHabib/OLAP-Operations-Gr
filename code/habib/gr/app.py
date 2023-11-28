import importlib
import argparse
import time

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from models.GestureModels import Gesture
from util.ExecuterManager import ExecuteManager
from util.PrinterManager import Printer
from util.Util import Util

encoding_file = 'utf-8'

model_property_name = 'model_asset_path'
num_hands_property_name = 'num_hands'
min_hand_detection_confidence_property_name = 'min_hand_detection_confidence'
min_hand_presence_confidence_property_name = 'min_hand_presence_confidence'
min_tracking_confidence_property_name = 'min_tracking_confidence'


def run(file_name: str, section_mediapipe_property_name: str, section_gesture_name: str):
    (model, num_hands, mhdc, mhpc,
     min_tracking_confidence) = (Util.get_mediapipe_gestures_recognizer_property(file_name,
                                                                                 section_mediapipe_property_name,
                                                                                 encoding_file))

    gesture_recognizer_result_list: list[Gesture] = []
    # initialize mediapipe

    gesture_recognizer_result = mp.tasks.vision.GestureRecognizerResult

    global FPS
    FPS = 0
    global time_fin
    time_fin = time.time_ns()
    # function that mp call
    def save_result(result: gesture_recognizer_result, output_image: mp.Image, timestamp_ms: int):
        gesture_recognizer_result_list.clear()
        Util.save(result, gesture_recognizer_result_list)
        #print('model launching execute...')
        Util.update_gestures_names(gestures=gesture_recognizer_result_list,
                                   file_path=file_name, gesture_section=section_gesture_name, )
        executor.update_gestures(gesture_recognizer_result_list)
        try:
            global FPS
            global time_fin
            FPS = 1/(((time.time_ns()-time_fin)/1000000000)+0.001)
        except:
            pass
        finally:
            time_fin = time.time_ns()

    # Initialize the gesture recognizer model
    base_options = python.BaseOptions(model_asset_path=model)
    options = vision.GestureRecognizerOptions(base_options=base_options, running_mode=vision.RunningMode.LIVE_STREAM,
                                              num_hands=num_hands, min_hand_detection_confidence=mhdc,
                                              min_hand_presence_confidence=mhpc, result_callback=save_result,
                                              min_tracking_confidence=min_tracking_confidence)
    recognizer = vision.GestureRecognizer.create_from_options(options)
    cap = cv2.VideoCapture(0)
    printer = Printer(cap, 'Output')
    executor = ExecuteManager()
    executor.start()
    time_fin = time.time_ns()
    #printer.start()
    while True:
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
        fps = str(int(FPS))
        printer.update(frame, gesture_recognizer_result_list)
        if (cv2.waitKey(1) == ord('q')
                or cv2.getWindowProperty("Output", cv2.WND_PROP_VISIBLE) < 1):
            break

    recognizer.close()
    cap.release()
    cv2.destroyAllWindows()
    executor.kill()


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--filename',
        help='Properties filename path',
        default='../../../utilities/config.property')
    parser.add_argument(
        '--section_property_mediapipe',
        help='Section mediapipe gesture recognition properties',
        default='DEFAULT')
    parser.add_argument(
        '--section_gesture_name',
        help='Section properties name of ',
        default='GESTURES')
    args = parser.parse_args()
    run(args.filename, args.section_property_mediapipe, args.section_gesture_name)


if __name__ == '__main__':
    main()
