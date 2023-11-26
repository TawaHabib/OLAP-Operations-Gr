from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks.python.components.containers.landmark import NormalizedLandmark


class HandProperty:
    def __init__(self, score, index, label):
        self.score: float = float(score)
        self.index: int = int(index)
        self.label: str = str(label)


class HandModel(object):

    def get_hand_position(self) -> list:
        pass

    def get_model_parameter(self) -> list:
        pass

    def get_hand_classification(self) -> int:
        pass

    def get_hand_name(self) -> str:
        pass

    def get_hand_property(self) -> HandProperty:
        pass


class HandSkeletalModel(HandModel):

    def __init__(self, hand_lm: list[NormalizedLandmark], property_hand: HandProperty):

        self.property_hand: HandProperty = property_hand
        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y,
                                            z=landmark.z) for landmark in hand_lm
        ])
        self.hand_normalized_landmark_list = hand_landmarks_proto
        x = []
        y = []

        for point in hand_lm:
            x.append(point.x)
            y.append(point.y)
        self.hand_lm = [x, y]

        x = 0
        y = 0
        for lmk in hand_lm:
            x += lmk.x
            y += lmk.y

        self.x = x/21
        self.y = y / 21
        self.hand_landmarks_list = []
        for point in hand_lm:
            self.hand_landmarks_list.append([point.x, point.y])

    def get_hand_lm_list(self) -> list[[float, float]]:
        return self.hand_landmarks_list

    def get_hand_position(self):
        return [self.x, self.y]

    def get_model_parameter(self) -> list[NormalizedLandmark]:
        return self.hand_normalized_landmark_list

    def get_hand_classification(self) -> int:
        return self.property_hand.index

    def get_hand_name(self) -> str:
        return self.property_hand.label

    def get_hand_property(self) -> HandProperty:
        return self.property_hand

