import os

def LOGO():
        # Development : 
        # return ../assets/logo/logo@100.png'

        # Production
        return './assets/logo/logo@100.png'

def ICON():
        #Development and Production
        return os.path.join(os.path.dirname(__file__), './assets/logo/logo@100.png')

def DATABASE():
        # Development: 
        # return '../database/datas.json'

        # Production
        return './database/datas.json'
