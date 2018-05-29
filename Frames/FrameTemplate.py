class FrameTemplate(object):

    def getPayload(self):
        """ Method for handle receive of new packet.
        :param packet:  The packet received in form of: |Preamble|Length
        :return:        Response of the packet, None if no response is required.
        """

    def __repr__(self):
        raise NotImplementedError

    def frame(self):
        raise NotImplementedError

    def printAndReturnNone(self, to_user):
        print(to_user)
        print(self)
        return None

    @classmethod
    def from_bytes(self, frame):
        raise NotImplementedError