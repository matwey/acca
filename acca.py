#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from acca.connection import Connection
from acca.producer import *
from acca.consumer import *
from acca.stream import *
from acca.parseopt import options

from sys import stdin, stdout

if __name__ == '__main__':
    opts = options()

    stream = RawStream(stdin, stdout)
    if opts["format"] == "bteo":
        stream = BTeoStream(stdin, stdout)

    producer = None
    consumer = None
    if opts["produce"]:
        producer = SingleShotProducer(opts["exchange"], opts["routing_key"], stream)
    if opts["rpc"]:
        consumer = RPCConsumer(producer, stream, opts["limit"])
        producer = None
    elif opts["consume"]:
        if opts["bind_exchange"] != "":
            consumer = ExchangeConsumer(opts["bind_exchange"], opts["binding_key"], stream, opts["limit"])
        else:
            consumer = QueueConsumer(opts["queue"], stream, opts["limit"])
    
    connection = Connection(opts["url"], producer = producer, consumer = consumer)
    connection.loop()

