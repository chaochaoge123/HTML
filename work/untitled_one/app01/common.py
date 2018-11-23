class MyResponse():
    def __init__(self):
        self.status=100
        self.time=None
        self.timezone=None
        self.msg=None

    def get_dic(self):
        return self .__dict__