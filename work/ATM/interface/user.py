from db import db_hander
from lib import common
user_logger= common.get_logger('用户日志')

def rejister_interface(name,password,balance=15000):
    user_dic = {'name':name,'password':password,'balance':15000,'xingyong':15000,'locked':False ,\
                'bankls':[],'shoppingcart':{}}
    db_hander .write_file(user_dic )
    user_logger .info('%s注册成功'%name)

def user_locked(name):
    user_dic=db_hander .read_file(name)
    user_dic ['locked']=True
    db_hander .write_file(user_dic )
    user_logger .info('%s已锁定'%(name))
