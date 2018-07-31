import json
import uuid

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
    """
    Add default cagetories for a new user
        :param user_uuid: string
        :return: void
    """
    default_names = ['Transport', 'Entertainment',
                        'Shopping', 'Bills', 'Personal care']

    user_info = Users.select_where('user_uuid', user_uuid)

    for name in default_names:
        Categories.insert_into(
            cat_name=name,
            cat_uuid=str(uuid.uuid4()),
            cat_total=0,
            cat_budget=0,
            user_id=user_info[0]['user_id']
        )

class AllCategories(PageHandler):
    @authorised_user
    def get(self, user_info=None):
        """
        Get all categories that belong to a user.
        If there is data, remove the `user_id` if each 
        entry and send response.
        If no data return an error message
            :param user_info: dict of user information
            :return: void
        """
        data = Categories.select_where('user_id', user_info['user_id'])
        if not data:
           self.json_response({'message': 'you have no categories'}, 404)
        else:
            for d in data:
                del d['user_id']
            
            self.json_response(json.dumps(data))


class Category(PageHandler):
    @authorised_user
    def post(self, user_info=None):
        """
        Adding a new category
            :params user_info: dict
            :return: void
        """
        data = json.loads(self.request.body)
        cat_exists = Categories.select_where('cat_name', data['cat_name'])
        if not cat_exists:
            Categories.insert_into(
                cat_name=data['cat_name'],
                cat_uuid=str(uuid.uuid4()),
                cat_total=0,
                cat_budget=data['cat_budget'],
                user_id=user_info[0]['user_id']
            )
            self.json_response({'message': 'category added'}, 201)
        else:
            self.json_response({'message': 'category already exists'}, 400)
    
    def put(self):
        """
        User can edit a category     
        """
        data = json.loads(self.request.body)
        Users.update_where(
            'cat_uuid', data['cat_uuid'],
            cat_name=data['cat_name'],
            cat_budget=data['cat_budget'])
        self.json_response(
            {'message': 'category updated'})
    
    def delete(self):
        """
        Deletes a category
        """
        data = json.loads(self.request.body)
        Categories.delete_where('cat_uuid', data['cat_uuid'])
        self.json_response({'message': 'Category deleted'})


