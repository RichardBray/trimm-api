import json

# Project Imports
from resources.helpers import PageHandler, authorised_user
from models.mysql import Categories, Users

'''
Transport
Eating Out
_Finances
Bills
Entertainment
Shopping
Holidays
_Family
Personal care
General
_Expenses
'''


def default_categories(user_uuid):
    '''
        Add default cagetories for a new user
    '''
    default_names = ['Transport', 'Entertainment',
                        'Shopping', 'Bills', 'Personal care']

    user_info = Users.select_where('user_uuid', user_uuid)

    for name in default_names:
        Categories.insert_into(
            cat_name=name,
            cat_budget=0,
            user_id=user_info[0]['user_id']
        )

class AllCategories(PageHandler):
    @authorised_user
    def get(self, user_info=None):
        '''
            Get all categories that belong to a user.
            If there is data, remove the `user_id` if each 
            entry and send response.
            If no data return an error message
        '''
        data = Categories.select_where('user_id', user_info['user_id'])
        if not data:
           self.json_response({'message': 'you have no categories'}, 404)
        else:
            for d in data:
                del d['user_id']
            
            self.json_response(json.dumps(data))


class Category(PageHandler):
    pass


class BudgetCategory(PageHandler):
    pass
