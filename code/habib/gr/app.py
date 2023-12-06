import argparse

from util.recognizer import Recognizer
from util.ExecuterManager import ExecuteManager


def run(file_name: str, section_mediapipe_property_name: str, section_gesture_name: str):
    execute = ExecuteManager()
    r = Recognizer(file_name, section_mediapipe_property_name, section_gesture_name, execute)
    r.start()


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
