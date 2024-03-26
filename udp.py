import socket
import json
import time

class UDP_discovery():
    def __init__(self, peer_id, network, broadcast, port):
        self.peer_id = peer_id
        self.broadcast = broadcast
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((network, self.port))
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def send_discovery_message(self):
        while True:
            message = {"command" : "hello", "peer_id" : self.peer_id}
            message_json = json.dumps(message).encode("utf-8")
            self.sock.sendto(message_json, (self.broadcast, self.port))
            time.sleep(5)

    def receive_responses(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            response = json.loads(data.decode("utf-8"))
            if response.get("status") == "ok" and response.get("peer_id") != self.peer_id:
                print("Received response from", addr, ":", response)
