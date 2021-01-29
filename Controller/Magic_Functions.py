import os
class Enviroment():
    def __init__(self,path):
        self.init_path = path
    
    def get_controller_path(self):
        return self.init_path + os.sep +"Controller"
    
    def get_view_path(self):
        return self.init_path + os.sep +"View"
    
    def get_model_path(self):
        return self.init_path + os.sep +"Model"
    
    def get_path(self):
        return self.init_path