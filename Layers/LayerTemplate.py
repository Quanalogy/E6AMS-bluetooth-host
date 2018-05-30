from Frames import FrameTemplate

class LayerTemplate:

    def __init__(self, frame_parser: FrameTemplate):
        self.frame_parser = frame_parser
        self.payload = None

    def send(self, packet):
        raise NotImplementedError
