# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import pika

class Connection(object):
    def __init__(self, url, producer = None, consumer = None):
        params = pika.URLParameters(url)
        self._connection = pika.SelectConnection(parameters=params,on_open_callback=self._on_open)
        self._producer = producer
        self._consumer = consumer

    def _on_open(self, connection):
        connection.channel(self._on_channel_open)
    
    def _on_channel_open(self, channel):
        if self._producer:
            self._producer.publish(channel)
        if self._consumer:
            self._consumer.consume(channel)

    def loop(self):
        try:
            self._connection.ioloop.start()
        except KeyboardInterrupt:
            self._connection.close()
            self._connection.ioloop.start()

