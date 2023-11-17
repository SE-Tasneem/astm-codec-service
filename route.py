from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import cgi
import decoder
import yaml
import sys

PORT_NUMBER = 8080
PUBLIC_ENTRY = './public/index.html'

# This class will handles any incoming request
class handleRoutes(BaseHTTPRequestHandler):
  # Handler for the POST requests
  def do_POST(self):
    if (self.path == '/'):
      file = open(PUBLIC_ENTRY)
      self.sendResponse(file.read(), 200, 'text/html')
      file.close()
      return
    if (self.path.startswith('/api/v1/')):
      if (self.path.endswith('decode-message')):
        # Read the content length to determine the size of the incoming data
        content_length = int(self.headers['Content-Length'])
        # Read the JSON data from the request body
        json_data = self.rfile.read(content_length)
        try:
          # Parse the JSON data
          data = json.loads(json_data)
          data = self.byteify(data)
          message = decode_message(data['message'])
          print(message)
        except ValueError as e:
          return self.sendResponse('Invalid JSON format: {}'.format(e), 400, 'application/json')
        decoded_message = decoder.decode_message(message)
        print(decoded_message)
        return self.sendResponse(decoded_message, 200, 'application/json')
      if (self.path.endswith('world')):
        return self.sendResponse('{"world": "hello"}', 200, 'application/json')
    else:
      return self.sendResponse('Not found.', 404, 'application/json')

  def sendResponse(self, res, status, type):
    self.send_response(status)
    self.send_header('Content-type', type)
    self.end_headers()
    # Send the html message
    self.wfile.write(res)
    return

  def byteify(self, input):
    if isinstance(input, dict):
        return {self.byteify(key): self.byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [self.byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input
def decode_message(encoded_message):
    # Remove commas and split the encoded message into pairs of two characters
    hex_pairs = encoded_message.replace(',', '').decode('hex')

    # Return the decoded message
    return hex_pairs
try:
  # Create a web server and define the handler to manage the incoming requests
  server = HTTPServer(('', PORT_NUMBER), handleRoutes)
  print('Started http server on port ' , PORT_NUMBER)
  # Wait forever for incoming http requests
  server.serve_forever()

except KeyboardInterrupt:
  print('\nFarewell my friend')
  server.socket.close()