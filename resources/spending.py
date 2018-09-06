import json
import uuid

# Project Imports
from resources.helpers import PageHandler, authorised_user
from models.mysql import Spending, Categories
from datetime import datetime

class SpendingItems(PageHandler):
    @authorised_user
    def post(self, user_info=None):
        """
        Gat all spending items that belong to the 
        logged in user. If data is retrieved from the database
        also get the category name based on the id and 
        return it.
        """
        data = json.loads(self.request.body)
        db_data = Spending.select_between_dates(
                date_field='create_dttm',
                field='user_id',
                start_date=data['start_date'],
                end_date=data['end_date'],
                field_val=user_info['user_id'])
        if not db_data:
            self.json_response({'message': 'no data'}, 404)
        else:
            for d in db_data:
                cat_data = Categories.select_where('cat_id', d['cat_id'])
                del d['user_id']
                del d['item_id']
                d['create_dttm'] = str(d['create_dttm'])
                d['cat_name'] = str(cat_data[0]['cat_name'])

            sorted_data = sorted(db_data, key=lambda item:item['create_dttm'], reverse=True)
            response = {'data': sorted_data}
            self.json_response(json.dumps(response))


class SpendingItem(PageHandler):

    @authorised_user
    def post(self, user_info=None):
        """
        Add a new spending item to the database
            :param user_info: dict user information
            :return: void
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
        self.json_response({'message': 'Item deleted'})
