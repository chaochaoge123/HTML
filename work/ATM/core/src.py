from db import db_hander
from interface import bank,shopping,user
from lib import common

info_name = {'name':None }
def rejister():
    print('注册')
    while True :
        zc_name = input('please input your name')
        if not db_hander .read_file(zc_name) :
            zc_pwd = input('输入密码')
            new_pwd= input('确认密码')
            if zc_pwd  == new_pwd :
                user.rejister_interface(zc_name ,zc_pwd )
                print('注册成功')
                break
            else:
                print('密码不一致')
                continue
        else:
            print('用户已存在')



def login():
    print('登录')
    if info_name['name']:
        print('用户已登录')
        return
    count = 0
    while True :
        dl_name = input('输入用户名')
        if count == 3:
            user.user_locked(dl_name)
            print('登录过多被锁定')
            break
        user_dic= db_hander .read_file(dl_name)
        if user_dic  :
            dl_password= input('输入密码')
            if user_dic ['password']== dl_password or  user_dic['locked'] == False :
                info_name ['name']= dl_name
                print('登录成功')
                common .get_logger('用户日志').info('%s登录成功'%(dl_name))
                break
            else:
                print('密码错误或者用户被锁定')
                count+=1
                continue
        else:
            print('用户名不存在')

@common.auth
def check_balance():
    print('查看余额')
    res=bank.check_balance_interface(info_name['name'])
    print(res)
@common.auth
def transfer():
    print('转账')
    while True :
        zz_name= input('输入转账对象')
        if zz_name ==info_name ['name']:
            print('不能给自己转账')
            continue
        if db_hander .read_file(zz_name ) :
            zz_balance= input('输入转账金额')
            if zz_balance .isdigit() :
                zz_balance =int(zz_balance)
                bank.transfer_interface(info_name['name'],zz_name ,zz_balance)
                print('转账成功')
                break
            else:
                print('输入数字啊，傻叉')
                continue
        else:
            print('转账对象不存在')

@common.auth
def repay():
    print('还款')
    while True :
        hk_balance = input('输入还款金额')
        if hk_balance .isdigit() :
            hk_balance = int(hk_balance )
            bank.repay_interface(info_name['name'],hk_balance )
            print('还款成功')
            break
        else:
            print('输入数字啊')

@common.auth
def withdram():
    print('取款')
    while True :
        balance= bank.check_balance_interface(info_name['name'])
        qk_balance= input('输入取款金额')
        if qk_balance .isdigit() :
            qk_balance =int(qk_balance)
            if balance >=qk_balance :
                bank.withdram_interface(info_name['name'],qk_balance )
                print('取款成功')
                break
            else:
                print('钱不够')
                continue
        else:
            print('输入错误')

@common.auth
def check_record():
    print('查看银行流水')
    info = bank.check_record_interface(info_name ['name'])
    print(info)
def shop():
    print('购物')
    msg = [
        ['coffee', 10],
        ['chicken', 20],
        ['iphone', 8000],
        ['macPro', 15000],
        ['car', 100000]
    ]
    shopping_cart= {}
    cost=0
    balance= bank.check_balance_interface(info_name['name'])
    while True :
        for bh,cp in enumerate(msg):
            print(bh,cp)
        bh_choice= input('输入购物编号,输入q,购物并退出')
        if bh_choice .isdigit() :
            bh_choice = int(bh_choice)
            if bh_choice <len(msg):
                cp_name= msg[bh_choice ][0]
                cp_jg= msg[bh_choice][1]
            else:
                print('输入错误')
                continue
            if balance >=cp_jg :
                if cp_name in shopping_cart :
                    shopping_cart [cp_name ]['count']+=1
                else:
                    shopping_cart[cp_name ]= {'prince':cp_name ,'count':1}
                balance -= cp_jg
                cost+= cp_jg
                print(cp_name +'已加入购物车',shopping_cart )
            else:
                print('钱不够')
        elif bh_choice =='q':
            cmd = input('是否购买 y or n')
            if cmd =='y':
                if balance >=cost:
                    res=shopping.shopping_interface(info_name['name'] ,cost,shopping_cart)
                    print('购物成功,商品信息',res )
                    break
                else:
                    print('钱不够')
                    break
            elif cmd== 'n':
                break
            else:
                print('输入错误')
        else:
            print('输入非法')

@common.auth
def look_shopping():
    print('查看购物车')
    res = shopping .look_shopping_interface(info_name['name'] )
    print(res)


info_dic={
       '1':rejister,
       '2': login,
       '3': check_balance,
       '4':transfer,
       '5': repay,
       '6':withdram,
       '7':check_record,
       '8':shop,
       '9': look_shopping
}


def run():
    while True:
        print('''
             1、注册
             2、登录
             3、查看余额
             4、转账
             5、还款
             6、取款
             7、查看银行流水
             8、购物
             9,、查看购物车
             ''')
        choice = input('请输入编号，输入q退出')
        if choice in info_dic:
            info_dic[choice]()
        elif choice == 'q':
            break
        else:
            print('输入错误')
