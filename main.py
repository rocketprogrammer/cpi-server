from twisted.internet import reactor, protocol
from ByteArray import ByteArray

class Client(protocol.Protocol):
    def connectionMade(self):
        self.server = self.factory
        self.server.clients.append(self)

    def dataReceived(self, rawData):
        print(rawData)
        reader = ByteArray(rawData)

        self.transport.write(b'')

class Server(protocol.ServerFactory):
    protocol = Client

    def __init__(self):
        self.clients = []

print('Starting server!')
server = Server()
reactor.listenTCP(9933, server)
reactor.run()