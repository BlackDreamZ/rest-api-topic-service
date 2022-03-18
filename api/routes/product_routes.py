from api.models.product_model import db, Product
from flask_restx import Resource


def init_route_product(app, rest_api):
    @rest_api.route('/api/product/get_all', doc={"description": "Метод для получения списка категорий"})
    @rest_api.response(404, 'Category list not found')
    @rest_api.response(200, 'Successful get category list ')
    class Category(Resource):
        """
           Return list category product

        """
        def post(self):

            result = {}
            list_category = db.session.query(Product).all()
            for elem in list_category:
                result[elem.id] = elem.name_category
            if not result:
                return {"success": False,
                        "msg": "Product list not found"}, 404
            return {"success": True,
                    "list_category":  result }, 200
