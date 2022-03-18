from api.routes.category_routes import init_route_categories
from api.routes.users_routes import init_route_users
from api.routes.product_routes import init_route_product

from flask_restx import Api


rest_api = Api(version="1.0", title="Users API")

def init_routes( _app, _rest_api ):
    init_route_categories ( _app, _rest_api )
    init_route_users( _app, _rest_api )
    init_route_product( _app, _rest_api  )
