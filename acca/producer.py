# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from acca.stream import Stream
import pika

class Producer(object):
    def __init__(self, stream):
        self._stream = stream
        if not isinstance(stream, Stream):
            raise TypeError("stream must be acca.stream.Stream")
    def publish(self, channel, props = None):
        pass

class SingleShotProducer(Producer):
    def __init__(self, exchange, routing_key, stream):
        super(SingleShotProducer, self).__init__(stream)
        self._exchange = exchange
        self._routing_key = routing_key
        self._stream = stream

    def publish(self, channel, props = pika.BasicProperties()):
        (_, message) = self._stream.get()
        channel.basic_publish(self._exchange, self._routing_key, message, props)

