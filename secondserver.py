
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from caseClasses import case_no_file
from caseClasses import case_existing_file
from caseClasses import case_always_fail
from caseClasses import case_dir_index_file
from caseClasses import case_dir_no_index_file


class RequestHandler(BaseHTTPRequestHandler):

  Cases = [case_no_file(),
           case_existing_file(),
           case_dir_index_file(),
           case_dir_no_index_file(),
           case_always_fail()]

#Handle a GET request
  def do_GET(self):
    try:    
      # What exactly is being requested?
      self.full_path = os.getcwd() + self.path
      print("FULL PATH: ", self.full_path)
      
      for case in self.Cases:
        handler = case
        if handler.test(self):
          print("CASE: ", case)
          handler.act(self)
          break
      
    except Exception as msg:
      self.handle_error(msg)


  def send_content(self, content, status=200):
    self.send_response(status)
    self.send_header("Content-Type", "text/html")
    self.send_header("Contenet-Length", str(len(content)))
    self.end_headers()
    self.wfile.write(content.encode('utf-8'))


  Error_Page = """\
    <html>
      <body>
        <h1>Error accessing {path}</h1>
        <p>{msg}</p>
      </body>
    </html>
  """  
  
  def handle_error(self, msg):
    content = self.Error_Page.format(path=self.path, msg=msg)
    self.send_content(content, 404)
    
    
  def handle_file(self, full_path):
    try:
      with open(full_path, 'rb') as reader:
        content = reader.read().decode()
      self.send_content(content)
    except IOError as msg:
      msg = "'{0}' cannot be read: {1}".format(self.path, msg)
      self.handle_error(msg)
  
  
  Listing_Page = '''\
    <html>
      <body>
        <ul>{0}</ul>
      </body>
    </html>
  '''
  
  def list_dir(self, full_path):
    try:
      entries = os.listdir(full_path)
      bullets = ['<li>{0}</li>'.format(e)
                 for e in entries if not e.startswith('.')]
      page = self.Listing_Page.format('\n'.join(bullets))
      self.send_content(page)
    except OSError as msg:
      msg = "'{0}' cannot be listed: {1}".format(self.path, msg)
      self.handle_error(msg)
    
    
    
#_______________________________________________

if __name__ == '__main__':
  server_address = ('127.0.0.1', 8080)
  server = HTTPServer(server_address, RequestHandler)
  server.serve_forever()