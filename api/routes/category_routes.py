from api.models.category_model import db, СategoriesProduct
from flask_restx import  Resource, fields
from flask import request

def init_route_categories(app, rest_api):
    @rest_api.route('/api/category/get_all', doc={"description": "Метод для получения списка категорий"})
    @rest_api.response(404, 'Category list not found')
    @rest_api.response(200, 'Successful get category list ')
    class CategoryList(Resource):
        """
           Return list category product

        """
        def post(self):

            result = {}
            list_category = db.session.query(СategoriesProduct).all()
            for elem in list_category:
                result[elem.id] = elem.name_category
            if not result:
                return {"success": False,
                        "msg": "Category list not found"}, 404
            return {"success": True,
                    "list_category":  result }, 200

    add_category = rest_api.model('AddCatrgoryModel', {"name_category": fields.String(required=True, min_length=2, max_length=32)
                                                  })
    @rest_api.route('/api/category/add')
    class AddCategory(Resource):
        """
           Creates a new user by taking 'signup_model_tg' input
        """

        @rest_api.expect(add_category, validate=True)
        def post(self):
            req_data = request.get_json()
            _name_category = req_data.get("name_category")
            print(_name_category )
            category_exists = СategoriesProduct.get_by_name(_name_category)
            if category_exists:
                return {"success": False,
                        "msg": "Name category already taken"}, 404

            new_category = СategoriesProduct(name_category=_name_category)
            new_category.save()

            return {"success": True,
                    "id": new_category.id,
                    "name_category": new_category.name_category,
                    "msg": "The category was successfully added"}
