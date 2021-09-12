#-*-coding:utf-8-*-
import math, struct, zlib


class ByteArrayException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


class ByteArray(Exception):
    LITTLE_ENDIAN = 0
    BIG_ENDIAN = 1

    def __init__(self, buf=None):
        self.stream = ""
        self.position = 0
        self.endian = ByteArray.BIG_ENDIAN
        self.length = 0
        self.availableSizes = 0

        if buf is None:
            raise ByteArrayException("can\'t read from empty byte stream")
        elif type(buf) == ByteArray:
            buf.setPosition(0)
            self.writeMulitiBytes(buf)
        elif type(buf) in (str, bytes):
            self.stream = buf
            self.length = len(buf)
            self.availableSizes = self.length
        else:
            print("[warning][ByteArray]buf type not supported")

    def bytesAvailable(self):
        return len(self.stream) > 0

    def toByteArray(self):
        return self.stream

    def convertStream(self):
        return [ord(c) for c in self.toByteArray()]

    def __readStream(self, size):
        buf = ""
        if self.availableSizes < size:  # If you have issues with this error, comment it out
            raise ByteArrayException("attempted to read with a size greater than length of byte stream")
        if size == 0:
            return buf
        buf = self.stream[self.position:self.position+size]
        self.position += size
        self.availableSizes = self.length - self.position
        return buf

    def __unpackStream(self, fmt, data):
        format = ""
        format += fmt
        buf = struct.unpack(format, data)
        return buf[0]

    def __writeStream(self, buf):
        head = self.stream[:self.position]
        end = self.stream[self.position:]
        self.stream = head + buf +end
        self.length = len(self.stream)
        self.position += len(buf)
        self.availableSizes = self.length - self.position

    def __packStream(self, fmt, data):
        format = ""
        if self.endian == ByteArray.BIG_ENDIAN:
            format += ">"
        else:
            format += "<"
        format += fmt
        buf = struct.pack(format, data)
        return buf

    def setPosition(self, pos):
        #if pos >= self.length:
            #raise ByteArrayException,"set position out of stream"
        self.position = pos
        self.availableSizes = self.length - self.position

    def getvalue(self):
        return self.stream

    def compress(self):
        lbuf = self.stream[:self.position]
        rbuf = self.stream[self.position:]
        rbuf = zlib.compress(rbuf)
        self.stream = lbuf + rbuf

    def decompress(self):
        lbuf = self.stream[:self.position]
        rbuf = self.stream[self.position:]
        rbuf = zlib.compress(rbuf)
        self.stream = lbuf + rbuf

    def readByte(self):
        buf = self.__readStream(1)
        res = self.__unpackStream("b", buf)
        return res

    def readBoolean(self):
        buf = self.__readStream(1)
        res = self.__unpackStream("?", buf)
        return True if res == 1 else False

    def readUnsignedByte(self):
        buf = self.__readStream(1)
        res = self.__unpackStream("B", buf)
        return res

    def readShort(self):
        buf = self.__readStream(2)
        res = self.__unpackStream("h", buf)
        return res

    def readUnsignedShort(self):
        buf = self.__readStream(2)
        res = self.__unpackStream("H", buf)
        return res

    def readLong(self):
        buf = self.__readStream(4)
        res = self.__unpackStream("l", buf)
        return res

    def readUnsignedLong(self):
        buf = self.__readStream(4)
        res = self.__unpackStream("L", buf)
        return res

    def readInt(self):
        buf = self.__readStream(4)
        res = self.__unpackStream("i", buf)
        return res

    def readUnsignedInt(self):
        buf = self.__readStream(4)
        res = self.__unpackStream("I", buf)
        return res

    def readInt64(self):
        buf = self.__readStream(8)
        res = self.__unpackStream("q", buf)
        return res

    def readUnsignedInt64(self):
        buf = self.__readStream(8)
        res = self.__unpackStream("Q", buf)
        return res

    def readFloat(self):
        buf = self.__readStream(4)
        res = self.__unpackStream("f", buf)
        return res

    def readDouble(self):
        buf = self.__readStream(8)
        res = self.__unpackStream("d", buf)
        return res

    def readUTF(self, nlen):
        buf = self.readShort()
        return self.readUTFBytes(nlen)

    def readUTFBytes(self, nlen):
        buf = self.__readStream(nlen)
        res = self.__unpackStream("%s"%nlen, buf)
        return res

    def readMulitiBytes(self, bytes, begin=0, nlen=-1):
        if bytes.length < begin:
            raise ByteArrayException("Write ByteArray position out")
        bytes.setPosition(begin)
        if nlen == -1:
            nlen = self.availableSizes
        bytes.readBytes(nlen)

    def readBytes(self, nlen):
        buf = self.__readStream(nlen)
        return buf

    def readBytesWithLength(self):
        length = self.readUnsignedInt()
        if length == 0xffffffff:
            return b""
        return self.__readStream(length)

    def readString(self):
        buf = self.readBytesWithLength()
        if self.endian == ByteArray.BIG_ENDIAN:
            return buf.decode("utf-16be")
        else:
            return buf.decode("utf-16le")

    def writeByte(self, value):
        buf = self.__packStream("b", value)
        self.__writeStream(buf)

    def writeBoolean(self, value):
        buf = self.__packStream("?", bool(value))
        self.__writeStream(buf)

    def writeUnsignedByte(self, value):
        buf = self.__packStream("B", value)
        self.__writeStream(buf)

    def writeShort(self, value):
        buf = self.__packStream("h", value)
        self.__writeStream(buf)

    def writeUnsignedShort(self, value):
        buf = self.__packStream("H", value)
        self.__writeStream(buf)

    def writeLong(self, value):
        buf = self.__packStream("l", value)
        self.__writeStream(buf)

    def writeUnsignedLong(self, value):
        buf = self.__packStream("L", value)
        self.__writeStream(buf)

    def writeInt(self, value):
        buf = self.__packStream("i", value)
        self.__writeStream(buf)

    def writeUnsignedInt(self, value):
        buf = self.__packStream("I", value)
        self.__writeStream(buf)

    def writeInt64(self, value):
        buf = self.__packStream("q", value)
        self.__writeStream(buf)

    def writeUnsignedInt64(self, value):
        buf = self.__packStream("Q", value)
        self.__writeStream(buf)

    def writeFloat(self, value):
        buf = self.__packStream("f", value)
        self.__writeStream(buf)

    def writeDouble(self, value):
        buf = self.__packStream("d", value)
        self.__writeStream(buf)

    def writeUTF(self, value):
        self.writeShort(len(value))
        self.writeUTFBytes(value)

    def writeUTFBytes(self, value):
        if isinstance(value, unicode):
            value = value.encode("utf-8")
        buf = self.__packStream("%ds"%len(value), value)
        self.__writeStream(buf)

    def writeMulitiBytes(self, bytes, begin=0, nlen=-1):
        bytes.setPosition(begin)
        if nlen == -1:
            nlen = self.availableSizes
        buf = bytes.readBytes(nlen)
        self.writeBytes(buf)

    def writeBytes(self, value):
        self.__writeStream(value)

    def writeChar(self, value):
        if len(value) != 1:
            raise ByteArrayException("Write char only accept bytes of length 1")
        self.__writeStream(value)

    def writeBytesWithLength(self, value):
        if not value:
            self.writeUnsignedInt(0xffffffff)
            return
        self.writeUnsignedInt(len(value))
        self.__writeStream(value)

    def writeString(self, value):
        if not value:
            self.writeBytesWithLength(b"")
            return
        if self.endian == ByteArray.BIG_ENDIAN:
            self.writeBytesWithLength(value.encode("utf-16be"))
        else:
            self.writeBytesWithLength(value.encode("utf-16le"))

    def writeInt24(self, value):
        high = math.floor(value / 0x10000)
        low = value - high * 0x10000
        offset = self.position
        self.writeByte(high)
        self.writeUnsignedShort(low)
        offset + 3
        print(self.convertStream())

    def writeInt40(self, value):
        high = math.floor(value / 0x100000000)
        low = value - high * 0x100000000
        offset = self.position
        self.writeByte(high)
        self.writeUnsignedInt(low)
        offset + 5
        print(self.convertStream())

    def writeInt48(self, value):
        high = math.floor(value / 0x100000000)
        low = value - high * 0x100000000
        offset = self.position
        self.writeShort(high)
        self.writeUnsignedInt(low)
        offset + 6
        print(self.convertStream())

    def writeInt56(self, value):
        temp = math.floor(value / 0x100000000)
        high = math.floor(temp / 0x10000)
        mid = temp - high * 0x10000
        low = value - temp * 0x100000000
        offset = self.position
        self.writeByte(high)
        self.writeUnsignedShort(mid)
        self.writeUnsignedInt(low)
        offset + 7
        print(self.convertStream())
