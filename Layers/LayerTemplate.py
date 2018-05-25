from Frames import FrameTemplate
class BaseLayerTemplate:

    def __init__(self, frame_parser: FrameTemplate):
        self.frame_parser = frame_parser
        self.payload = None

    def receive(self, packet):
        raise NotImplementedError

class LayerTemplate(BaseLayerTemplate):

    def bind(self, lower_layer: BaseLayerTemplate):
        self.lower_layer = lower_layer