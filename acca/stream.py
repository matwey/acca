# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from message import Message, RawMessage, BTeoMessage
from pika import BasicProperties
from construct import *

class Stream(object):
    def __init__(self, inp, out):
        self._inp = inp
        self._out = out
    
    def get(self):
        pass
    def put(self, properties, body):
        pass


class RawStream(Stream):
    def __init__(self, inp, out):
        super(RawStream, self).__init__(inp, out)

    def get(self):
        message = self._inp.read()
        return (BasicProperties(), message)
    def put(self, properties, body):
        self._out.write(str(RawMessage(properties.timestamp, body)))

class BTeoStream(Stream):
    _bteo_message = ExprAdapter(Struct("bteo_message",
        UBInt32("version"),
        UBInt32("status"),
        CString("comment"),
        CString("payload")),
        encoder = lambda obj,ctx: obj,
        decoder = lambda obj,ctx: (obj.version, obj.status, obj.comment, obj.payload)
    )

    def __init__(self, inp, out):
        super(BTeoStream, self).__init__(inp, out)
    
    def get(self):
        version = 1
        status = 0
        comment = u""

        message = self._inp.read()
        lines = message.splitlines(True)
        
        while len(lines):
            x = lines[0]
            header = x.split(":",2)
            if len(header) == 2:
                [key, value] = header
                key = key.strip()
                value = value.strip()
                if key == "Version":
                    version = int(value)
                elif key == "Status":
                    status = int(value,0)
                elif key == "Comment":
                    comment = str(value)
                del lines[0]
            else: # No more headers
                break

        payload = "".join(lines)
        
        return (BasicProperties(), BTeoStream._bteo_message.build(Container(version=version, status=status, comment=comment, payload=payload)))

    def put(self, properties, body):
        (version, status, comment, payload) = BTeoStream._bteo_message.parse(body)
        self._out.write(str(BTeoMessage(properties.timestamp, version, status, comment, payload)))
