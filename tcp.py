import json
import socket

class TCP_Communication():
    def __init__(self, peer_id, peer_ip, peer_port):
        self.peer_id = peer_id
        self.peer_ip = peer_ip
        self.peer_port = peer_port
        self.message_history = {}

    def send_message(self, tcp_socket, message):
        message_bytes = json.dumps(message).encode('utf-8')
        tcp_socket.sendall(message_bytes)

    def receive_message(self, tcp_socket):
        data = tcp_socket.recv(4096)
        if data:
            return json.loads(data.decode('utf-8'))
        else:
            return None

    def perform_handshake(self, tcp_socket):
        handshake_request = {"command": "hello", "peer_id": self.peer_id}
        self.send_message(tcp_socket, handshake_request)
        response = self.receive_message(tcp_socket)
        return response

    def send_new_message(self, tcp_socket, message_id, message):
        new_message_request = {"command": "new_message", "message_id": message_id, "message": message}
        self.send_message(tcp_socket, new_message_request)
        response = self.receive_message(tcp_socket)
        return response

    def communicate_with_peer(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
            try:
                tcp_socket.connect((self.peer_ip, self.peer_port))
                handshake_response = self.perform_handshake(tcp_socket)
                if handshake_response and handshake_response.get("status") == "ok":
                    print("Handshake successful with peer:", self.peer_id)
                    self.message_history.update(handshake_response.get("messages", {}))
                    for message_id, message_content in self.message_history.items():
                        self.send_new_message(tcp_socket, message_id, message_content['message'])
                        print("Sent message:", message_content['message'])
            except ConnectionRefusedError:
                print("Connection refused to peer:", self.peer_id)
