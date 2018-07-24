import json
import uuid

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
            for d in data:
                cat_data = Categories.select_where('cat_id', d['cat_id'])
                del d['user_id']
                del d['item_id']
                d['create_dttm'] = str(d['create_dttm'])
                d['cat_name'] = str(cat_data[0]['cat_name'])

            self.json_response(json.dumps(data))


class SpendingItem(PageHandler):
    @authorised_user
    def post(self, user_info=None):
        """
            Add a new spending item to the database
        """
        data = json.loads(self.request.body)
        Spending.insert_into(
            item_uuid=str(uuid.uuid4()),
            item_name=data['item_name'],
            item_price=data['item_price'],
            create_dttm=data['create_dttm'],
            user_id=user_info['user_id'],
            cat_id=data['cat_id'])

        self.json_response({'message': 'spending item created'}, 201)

    def put(self):
        data = json.loads(self.request.body)
        updated_values = {
            'item_name': data['item_name'],
            'item_price': data['item_price'],
            'create_dttm': data['create_dttm'],
            'cat_id': data['cat_id'],
        }
        Spending.update_where(
            'item_uuid', data['item_uuid'], **updated_values)
        self.json_response({'message': 'Item has been updated'})

    def delete(self):
        data = json.loads(self.request.body)
        Spending.delete_where('item_uuid', data['item_uuid'])
        self.json_response({'message': 'Item was deleted'})
