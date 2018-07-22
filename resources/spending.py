import json
from resources.helpers import PageHandler, authorised_user
from models.mysql import Spending, Users


class SpendingItems(PageHandler):
    '''
        Gat all spending items that belong to the 
        logged in user.
    '''
    @authorised_user
    def get(self, user_info=None):
        data = Spending.select_where('user_id', user_info[0]['user_id'])
        if not data:
            self.json_response({'message': 'no data'}, 404)
        else:
            self.json_response(json.dumps(data))


class SpendingItem(PageHandler):
    '''
        Add a new spending item to the database
    '''
    @authorised_user
    def post(self):
        data = json.loads(self.request.body)
        Spending.insert_into(
            item_name=data['item_name'],
            item_price=data['item_price'],
            create_dttm=data['create_dttm'],
            user_id='user_info[user_id]',
            cai_id='cat_name')

        self.json_response({'message': 'spending item created'}, 201)
