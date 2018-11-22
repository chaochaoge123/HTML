from db import db_hander
from lib import common

bank_logger= common.get_logger('银行日志')


def check_balance_interface(name):
    user_dic=db_hander.read_file(name)
    return  user_dic ['balance']

def transfer_interface(from_name,to_name,balance):
    user_from_name=db_hander.read_file(from_name )
    user_to_name = db_hander.read_file(to_name )
    user_from_name ['balance']-= balance
    user_to_name ['balance']+=balance
    user_from_name ['bankls'].append('%s向%s转账%s'%(from_name,to_name,balance))
    user_to_name ['bankls'].append('%s收到%s的转账%s'%(to_name,from_name,balance))
    db_hander .write_file(user_from_name )
    db_hander .write_file(user_to_name )
    bank_logger.info('%s 成功转账%s' %(from_name ,balance ))


def repay_interface(name,balance):
    user_dic=db_hander .read_file(name)
    user_dic ['balance']+=balance
    user_dic['bankls'].append('%s还款%s'%(name,balance))
    db_hander .write_file(user_dic )
    bank_logger.info('%s还款%s' % (name, balance))

def withdram_interface(name,balance):
   user_dic= db_hander .read_file(name)
   user_dic ['balance']-=balance
   user_dic['bankls'].append('%s取款%s' % (name, balance))
   db_hander .write_file(user_dic )
   bank_logger.info('%s取款%s' % (name, balance))

def check_record_interface(name):
    user_dic=db_hander .read_file(name)
    return user_dic ['bankls']