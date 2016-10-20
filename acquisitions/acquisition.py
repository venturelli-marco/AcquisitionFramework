from model.frameSet import frameSet

RESOLUTION_VGA = 3.0
RESOLUTION_FULLHD = 1.0
RESOLUTION_QVGA = 6.0
RESOLUTION_HD = 1.5
RESOLUTION_HD1600 = 1.2

RESOLUTION_DEPTH = (424, 512)

class Acquisition:

    def get_frame(self, frame):
        if not isinstance(frame, frameSet):
            raise TypeError("Given argument is not an istance of frameset")
        self._get_frame(frame)

    def _get_frame(self, frame):
        pass