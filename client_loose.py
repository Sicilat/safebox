import socket, time
SERVER = "127.0.0.1"
PORT = 8080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
out_data = [0, 0]
	
def ask_credentials():
	out_data[0] = input('Username > ')
	out_data[1] = input('Password > ')
	client.sendall(bytes(out_data[0],'UTF-8'))
	time.sleep(0.1)
	client.sendall(bytes(out_data[1],'UTF-8'))

ask_credentials()
client.close()