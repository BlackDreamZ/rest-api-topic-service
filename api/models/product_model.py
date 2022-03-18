from flask_sqlalchemy import SQLAlchemy
from api.models import db

# Таблица Товар
class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    created_at = db.Column(db.DateTime(), nullable=False)
    name_product = db.Column(db.String(64), nullable=False)
    price = db.Column(db.String(64), nullable=False)
    category_id = db.Column(db.Integer(), db.ForeignKey('Сategories_product.id'))

    def update_name_product(self, new_name_product):
        self.name_product = new_name_product

    def update_price(self, new_price):
        self.price = new_price

    def update_category_id(self, new_id):
        self.category_id = new_id

    def __repr__(self):
        return "Expired Product: {self.jwt_token}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
            return cls.query.get_or_404(id)