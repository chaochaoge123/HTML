from db import db_hander
from lib import common

shopping_logger =common.get_logger('购物日志')
def shopping_interface(name,cost,shoppingcart):
    user_dic=db_hander.read_file(name)
    user_dic ['balance']-=cost
    shopping_logger .info('购物扣款成功')
    user_dic ['shoppingcart']= shoppingcart
    db_hander .write_file(user_dic )
    return user_dic ['shoppingcart']


def look_shopping_interface(name):
    user_dic=db_hander .read_file(name)
    return user_dic ['shoppingcart']
