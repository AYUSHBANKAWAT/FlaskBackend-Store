from flask import Flask, request
from flask_restful import Resource, Api,reqparse
from flask_jwt import JWT,jwt_required
from security import authenticate,identify

app = Flask(__name__)
app.secret_key = 'psajsndks'
api = Api(app)

jwt = JWT(app,authenticate,identify)

items=[]

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
    'price',
     type=float,
     required=True,
     help="This field cannot be left blank"
     )
    
    @jwt_required()
    def get(self,name):
        item = next(filter(lambda x :x['name']==name,items),None)
        return {'item':item}, 200 if item else 404
    
    def post(self,name):
        requesData = Item.parser.parse_args()
        if next(filter(lambda x :x['name']==name,items),None) is not None:
            return ({'message':"An item with this name '{}' already exist".format(name)}), 400
        else:
            requesData = request.get_json()
            item = {'name':name,'price':requesData['price']}
            items.append(item)
            return item, 201
        
    def delete(self,name):
        global items
        items =  list(filter(lambda x: x['name']!=name,items))
        return {"message":"Item named as '{}' is deleted".format(name)}
    
    def put(self,name):
        requestData = Item.parser.parse_args()
        item = next(filter(lambda x :x['name']==name,items),None)
        if item is None:
            item={'name':name,'price':requestData['price']}
            items.append(item)
        else:
            item.update(requestData['price'])
        return item 
            
    
class ItemLsit(Resource):
    def get(self):
        return {'items':items}
        
api.add_resource(ItemLsit,'/items')    
api.add_resource(Item,'/item/<string:name>')
app.run(port=5000,debug=True)
