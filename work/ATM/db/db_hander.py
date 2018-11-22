from conf import settings
import json
import os

def read_file(name):
    user_path= os.path.join(settings .DB_path,'%s.json'%(name) )
    if os.path.exists(user_path):
        with open(user_path ,'rt',encoding='utf-8')as f:
           return  json.load(f)
    else:
        return False

def write_file(user_dic):
    user_path=os.path.join(settings .DB_path,'%s.json' %user_dic['name'] )
    with open(user_path ,'wt',encoding= 'utf-8')as f:
        json.dump(user_dic ,f)
        f.flush()
