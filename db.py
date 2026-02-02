import os

PATHS = ['instances/']
def initialize():
    for d in PATHS:
        try:
            os.makedir(d)
        except FileExistsError:
            pass
        
        
    
