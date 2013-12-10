# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from optparse import OptionParser, OptionGroup
from os import environ

def options():
    parser = OptionParser()

    parser.add_option("--format", action="store", type="string", dest="format",
        help="Message format type. (use also ACCA_FORMAT environment variable)",
        metavar="raw|bteo", default=environ.get("ACCA_FORMAT","bteo"))

    amqp_group = OptionGroup(parser, "AMQP Options")
    amqp_group.add_option("--url", action="store", type="string", dest="url",
        help="Connection options specified in the form of URL. (use also ACCA_URL environment variable)",
        metavar="amqp://guest:guest@rabbit-server1:5672/%2F",
        default=environ.get("ACCA_URL","amqp://guest:guest@localhost:5672/%2F"))
    parser.add_option_group(amqp_group)

    producer_group = OptionGroup(parser, "Producer Options")
    producer_group.add_option("-p", "--produce", action="store_true", dest="produce",
        help="Produce the message", default=False),
    producer_group.add_option("-x", "--exchange", action="store", type="string", dest="exchange",
        help="Exchange to publish the message", default="")
    producer_group.add_option("--routing_key", action="store", type="string", dest="routing_key",
        help="Routing key to publish the message with", default="")
    producer_group.add_option("--rpc", action="store_true", dest="rpc",
        help="Use RPC pattern and wait for an answer", default=False)
    parser.add_option_group(producer_group)

    consumer_group = OptionGroup(parser, "Consumer Options")
    consumer_group.add_option("-c", "--consume", action="store_true", dest="consume",
        help="Consume the messages", default=False)
    consumer_group.add_option("--bind_exchange", action="store", type="string", dest="bind_exchange",
        help="Exchange to bind to", default="")
    consumer_group.add_option("--binding_key", action="store", type="string", dest="binding_key",
        help="Binding key to bind with", default="")
    consumer_group.add_option("-q", "--queue", action="store", type="string", dest="queue",
        help="Queue to consume from", default="")
    consumer_group.add_option("-n", "--limit", action="store", type="int", dest="limit",
        help="Number of messages to wait for (default 1)",
        metavar="NUM", default=1)
    parser.add_option_group(consumer_group)

    (options, args) = parser.parse_args()

    if options.format != "raw" and options.format != "bteo":
        parser.error("option --format must be either raw or bteo")

    if options.rpc and options.consume:
        parser.error("options --rpc and --consume are mutually exclusive")

    if options.bind_exchange and options.queue:
        parser.error("options --queue and --bind_exchange are mutually exclusive")

    return options.__dict__

