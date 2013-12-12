# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from os import linesep

class Message(object):
    def __init__(self, time):
        self._time = time

class RawMessage(Message):
    def __init__(self, time, payload):
        super(RawMessage, self).__init__(time)
        self._payload = payload

    def __str__(self):
        return linesep.join(map(str,[self._time,self._payload])) + linesep

class BTeoMessage(Message):
    def __init__(self, time, version, status, comment, payload):
        super(BTeoMessage, self).__init__(time)
        self._version = version
        self._status = status
        self._comment = comment
        self._payload = payload
    
    def __str__(self):
        header = "%d %x %s" % (self._version,self._status,self._comment)
        return linesep.join(map(str,[self._time, header, self._payload])) + linesep

