import ServerException
import os

class case_existing_file(object):
    def test(self, handler):
      return os.path.isfile(handler.full_path)
  
    def act(self, handler):
      handler.handle_file(handler.full_path)
      
      
class case_no_file(object):
    def test(self, handler):
      return not os.path.exists(handler.full_path)
  
    def act(self, handler):
      raise ServerException("'{0}' not found".format(handler.path))
    
    
class case_always_fail(object):
    def test(self, handler):
      return True
  
    def act(self, handler):
      raise ServerException("Unknown object '{0}'".format(handler.path))    
    
    
class case_dir_index_file(object):
    def index_path(self, handler):
      return os.path.join(handler.full_path, 'index.html')
  
    def test(self, handler):
      return os.path.isdir(handler.full_path) and \
            os.path.isfile(self.index_path(handler))
    
    def act(self, handler):
      handler.handle_file(self.index_path(handler))
      
      
class case_dir_no_index_file(object):
    def index_path(self, handler):
      return os.path.join(handler.full_path, 'index.html')
  
    def test(self, handler):
      return os.path.isdir(handler.full_path) and \
            not os.path.isfile(self.index_path(handler))
    
    def act(self, handler):
      handler.list_dir(handler.full_path)