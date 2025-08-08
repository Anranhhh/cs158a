import ssl
import socket
import gzip
import io

host = "www.google.com"
port = 443
Request = (
    "GET / HTTP/1.1\r\n"
    f"Host: {host}\r\n"
    "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36\r\n"
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
    "Accept-Encoding: gzip\r\n"
    "Connection: close\r\n\r\n"
)
bufSize = 4096
outputFile = "response.html"

# Reads HTTP response headers from the SSL socket
def read_headers(sock):
    data = bytearray()
    while b"\r\n\r\n" not in data: # keep reading until the end of the header
        chunk = sock.recv(bufSize)
        if not chunk:
            break
        data += chunk
    header, _, rest = data.partition(b"\r\n\r\n")
    return header.decode(), rest # Return header text and remaining bytes

# Process HTTP's chunked encoding
def unchunkBody(body_bytes):
    out = bytearray()
    bio = memoryview(body_bytes)
    while True:
        newLine = bio.tobytes().find(b"\r\n")
        size = int(bio[:newLine].tobytes(), 16)
        if size == 0:
            break
        start = newLine + 2
        out += bio[start : start + size]
        bio = bio[start + size + 2 :]
    return bytes(out)

def main():
    context = ssl.create_default_context()
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            ssock.sendall(Request.encode())

            # Call read_header method to split header & body
            header_text, body = read_headers(ssock)
        
            # Store the parsed headers in key-value form
            headers = {}
            for line in header_text.split("\r\n")[1:]:
                key, value = line.split(":", 1)
                headers[key.lower()] = value.strip()

            # Read rest of body
            while True:
                chunk = ssock.recv(bufSize)
                if not chunk:
                    break
                body += chunk

    # If the HTTP server sent response in chunked encoding, 
    # need to remove chunk-size markers.
    if headers.get("transfer-encoding", "") == "chunked":
        body = unchunkBody(body)
    
    # Decompress content that was compressed by HTTP server
    if headers.get("content-encoding") == "gzip":
        body = gzip.decompress(body)
    
    with open(outputFile, "wb") as f:
        f.write(body)

    print(f"File is saved to '{outputFile}'")

if __name__ == "__main__":
    main()
