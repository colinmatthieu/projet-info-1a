from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class EchoHttpHandlerWithPOST(BaseHTTPRequestHandler):
  data = {}

  def do_GET(self):
    client_addr = self.client_address
    request_path = self.path

    params = request_path.split("/")
    if len(params) != 3:
      self.send_response(400)
      return
    name = params[2].replace("%20", " ")

    self.send_response(200)
    self.send_header(b'Content-type', b'text/html')
    self.end_headers()
    token = self.data[name]
    self.wfile.write(
      f"<html><body>Salut {name} from {client_addr}\n votre code: {token}\n<h2>Nous sommes:des gens</h2></body></html>"
      .encode())

  def do_POST(self):
    client_addr = self.client_address
    request_path = self.path
    data_size = int(self.headers["Content-Length"])
    self.log_message(f"data_size = {data_size}")
    data = self.rfile.read(data_size).decode()
    import json
    t = json.loads(data)
    self.data[t["name"]] = t["secret"]
    print(self.data)

    # = json.loads( data_json )
    self.send_response(200)
    self.send_header(b'Content-type', b'text/html')
    self.end_headers()
    #self.wfile.write( f"Server receive POST request {request_path} from {client_addr} with data {data}".encode())
    self.wfile.write(
      f"Server receive POST request {request_path} from {client_addr} with data {data}"
      .encode())


server = HTTPServer(("", 8000), EchoHttpHandlerWithPOST)
server.serve_forever()
