# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import pika

class Consumer(object):
    def __init__(self, stream, limit):
        self._stream = stream
        self._limit = limit
    def consume(channel):
        pass

class QueueConsumer(Consumer):
    def __init__(self, queue, stream, limit):
        super(QueueConsumer, self).__init__(stream, limit)
        self._queue = queue

    def _on_message(self, channel, method, properties, body):
        self._limit = self._limit - 1
        self._stream.write(body)
        channel.basic_ack(delivery_tag = method.delivery_tag)
        if self._limit == 0:
            def _on_cancelok(frame):
                channel.close()
            channel.basic_cancel(_on_cancelok, self._consumer_tag)

    def consume(self, channel):
        self._consumer_tag = channel.basic_consume(self._on_message, queue=self._queue)

class ExchangeConsumer(QueueConsumer):
    def __init__(self, exchange, binding_key, stream, limit):
        super(ExchangeConsumer, self).__init__(None, stream, limit)
        self._exchange = exchange
        self._binding_key = binding_key

    def consume(self, channel):
        def _on_bindok(frame):
            super(ExchangeConsumer, self).consume(channel)
        def _on_queue_declareok(frame):
            self._queue = frame.method.queue
            channel.queue_bind(_on_bindok, self._queue, self._exchange, self._binding_key)
    
        channel.queue_declare(_on_queue_declareok, exclusive=True, auto_delete=True)

class RPCConsumer(QueueConsumer):
    def __init__(self, producer, stream, limit):
        super(RPCConsumer, self).__init__(None, stream, limit)
        self._producer = producer
    
    def consumer(self, channel):
        def _on_queue_declareok(frame):
            self._queue = frame.method.queue
            self._producer.publish(channel, pika.BasicProperties(reply_to = self._queue))
            super(RPCConsumer, self).consume(channel)
    
        channel.queue_declare(_on_queue_declareok, exclusive=True, auto_delete=True)

