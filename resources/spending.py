import json

# Project Imports
from resources.helpers import PageHandler, authorised_user
from models.mysql import Spending, Categories
from datetime import datetime

class SpendingItems(PageHandler):
    @authorised_user
    def get(self, user_info=None):
        '''
            Gat all spending items that belong to the 
            logged in user. If data is retrieved from the database
            also get the category name based on the id and 
            return it.
        '''
        data = Spending.select_where('user_id', user_info['user_id'])
        if not data:
            self.json_response({'message': 'no data'}, 404)
        else:
            cat_data = Categories.select_where('cat_id', data[0]['cat_id'])
            data[0]['create_dttm'] = str(data[0]['create_dttm'])
            data[0]['cat_name'] = str(cat_data[0]['cat_name'])
            self.json_response(json.dumps(data))


class SpendingItem(PageHandler):
    @authorised_user
    def post(self, user_info=None):
        '''
            Add a new spending item to the database
        '''
        data = json.loads(self.request.body)
        Spending.insert_into(
            item_name=data['item_name'],
            item_price=data['item_price'],
            create_dttm=datetime.utcnow(),
            user_id=user_info['user_id'],
            cat_id=data['cat_id'])

        self.json_response({'message': 'spending item created'}, 201)
