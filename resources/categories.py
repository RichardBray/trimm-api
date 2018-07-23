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

class UserCategories(PageHandler):

    def get(self):
        '''
            Get all categories that belong to a user
        '''
        pass
