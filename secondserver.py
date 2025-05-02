from http.server import BaseHTTPRequestHandler, HTTPServer
import os

class ServerException(Exception):
  pass


class RequestHandler(BaseHTTPRequestHandler):
  "'Handle HTTP requests by returning a fixed page.'"
  # Page to send back
  Page = '''\
      <html>
        <body>
          <table>
            <tr>  <td>Header</td>        <td>Value</td>         </tr>
            <tr>  <td>Date and time</td> <td>{date_time}</td>   </tr> 
            <tr>  <td>Client host</td>   <td>{client_host}</td> </tr>
            <tr>  <td>Client port</td>   <td>{client_port}</td> </tr> 
            <tr>  <td>Command</td>       <td>{command}</td>     </tr>
            <tr>  <td>Path</td>          <td>{path}</td>        </tr> 
          </table>
        </body>
      </html>
    '''


#Handle a GET request
  def do_GET(self):
    try:    
      # What exactly is being requested?
      full_path = os.getcwd() + self.path
      print("Current directory: ", full_path)
      
      if not os.path.exists(full_path):
        raise ServerException("'{0}' not found".format(self.path))
      
      elif os.path.isfile(full_path):
        self.handle_file(full_path)
        
      else:
        raise ServerException("Unknown object '{0}'".format(self.path))
      
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
        content = reader.read()
      self.send_content(content)
    except IOError as msg:
      msg = "'{0}' cannot be read: {1}".format(self.path, msg)
      self.handle_error(msg)
    
    
  def create_page(self):
    values = {
      'date_time'   : self.date_time_string(),
      'client_host' : self.client_address[0],
      'client_port' : self.client_address[1],
      'command'     : self.command,
      'path'        : self.path 
    }
    page = self.Page.format(**values)
    return page
    
#_______________________________________________

if __name__ == '__main__':
  server_address = ('127.0.0.1', 8080)
  server = HTTPServer(server_address, RequestHandler)
  server.serve_forever()