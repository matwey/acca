from acca.stream import *
import unittest
from io import BytesIO
from pika import BasicProperties
from datetime import datetime
from os import linesep

class StreamTest(unittest.TestCase):
	def setUp(self):
		pass
	def test_raw_message(self):
		istr = "Raw input data\nGoes untouched"
		timestamp = datetime(2013,10,10,18,35,44)

		inp = BytesIO(istr)
		out = BytesIO()

		stm = RawStream(inp, out)
		(props, mstr) = stm.get()
		self.assertEqual(mstr,istr)
		stm.put(BasicProperties(timestamp=timestamp),istr)
		self.assertEqual(linesep.join([str(timestamp),istr])+linesep,out.getvalue())
	def _bteo_message_helper1(self, lines, binary):
		istr = linesep.join(lines)

		inp = BytesIO(istr)
		out = BytesIO()

		stm = BTeoStream(inp, out)
		(props, mstr) = stm.get()
		self.assertEqual(mstr, binary)
	def _bteo_message_helper2(self, text, binary, timestamp):
		inp = BytesIO()
		out = BytesIO()

		stm = BTeoStream(inp, out)
		stm.put(BasicProperties(timestamp=timestamp),binary)
		self.assertEqual(text, out.getvalue())
	def _bteo_message_helper_failure(self, lines):
		istr = linesep.join(lines)

		inp = BytesIO(istr)
		out = BytesIO()

		stm = BTeoStream(inp, out)
		self.assertRaises(ValueError, stm.get)
	def test_bteo_message1(self):
		istr = "Raw input data\nGoes untouched"
		lines = [istr]
		self._bteo_message_helper1(lines, "\x00\x00\x00\x01\x00\x00\x00\x00\x00"+istr+"\x00")
	def test_bteo_message2(self):
		istr = "Raw input data\nGoes untouched"
		lines = ["Version: 256",istr]
		self._bteo_message_helper1(lines, "\x00\x00\x01\x00\x00\x00\x00\x00\x00"+istr+"\x00")
	def test_bteo_message3(self):
		istr = "Raw input data\nGoes untouched"
		lines = ["Version: 256","Version: 255",istr]
		self._bteo_message_helper1(lines, "\x00\x00\x00\xFF\x00\x00\x00\x00\x00"+istr+"\x00")
	def test_bteo_message4(self):
		istr = "Raw input data\nGoes untouched"
		lines = ["Status: 256",istr]
		self._bteo_message_helper1(lines, "\x00\x00\x00\x01\x00\x00\x01\x00\x00"+istr+"\x00")
	def test_bteo_message_failure(self):
		istr = "Raw input data\nGoes untouched"
		lines = ["Status: aaaabbbb",istr]
		self._bteo_message_helper_failure(lines)
	def test_bteo_message5(self):
		istr = "Raw input data\nGoes untouched"
		lines = ["Status: 0x00000100",istr]
		self._bteo_message_helper1(lines, "\x00\x00\x00\x01\x00\x00\x01\x00\x00"+istr+"\x00")
	def test_bteo_message6(self):
		istr = "RoBurToVoy goes untouched"
		comment = "RoBurToVoy"
		lines = ["Comment : " + comment,istr]
		self._bteo_message_helper1(lines, "\x00\x00\x00\x01\x00\x00\x00\x00"+comment+"\x00"+istr+"\x00")
	def test_bteo_message7(self):
		timestamp = datetime(2013,10,10,18,35,44)

		self._bteo_message_helper2(linesep.join([str(timestamp),"1 0 ","",""]), "\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00", timestamp)
	def test_bteo_message7(self):
		timestamp = datetime(2013,10,10,18,35,44)

		self._bteo_message_helper2(linesep.join([str(timestamp),"1 ce Comment","Payload",""]), "\x00\x00\x00\x01\x00\x00\x00\xceComment\x00Payload\x00", timestamp)

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(StreamTest)
	unittest.TextTestRunner(verbosity=2).run(suite)

