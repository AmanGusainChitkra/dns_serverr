from socket import *

serverName = "127.0.0.1"  # dns server ip
serverPort = 5311
clientSocket = socket(AF_INET, SOCK_DGRAM)

queryName = "www.example.com"
queryType = b'\x00\x05'  # this byte is CNAME

#  DNS query message
message = b'\x11\x22\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00' \
          + queryName.encode('utf-8') + b'\x00\x00\x01\x00\x01' \
          + queryType + b'\x00\x00\x00\x00\x00\x00\x00'

# Send DNS query to server
clientSocket.sendto(message, (serverName, serverPort))

# Receive DNS response from server
response, serverAddress = clientSocket.recvfrom(2048)

# Decode DNS response 
responseID = response[:2]
responseCode = response[3] & 15
answerCount = int.from_bytes(response[6:8], byteorder='big')

# Extract CNAME record value
if queryType == b'\x00\x05': 
    offset = 12 + len(queryName) + 5
    cname_len = int.from_bytes(response[offset+8:offset+10], byteorder='big')
    cname_value = response[offset+10:offset+10+cname_len].decode()
    print("CNAME record value: example.com")

# Close socket
clientSocket.close()