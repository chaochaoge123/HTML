from django.middleware.security import  MiddlewareMixin
class MyMiddle(MiddlewareMixin ):
    def process_response(self,request,response):
        if request .method=='OPTIONS':
            response['Access-Control-Allow-Methods'] = '*'
            response['Access-Control-Allow-Headers'] = '*'

        response['Access-Control-Allow-Origin'] = '*'
        return response




























