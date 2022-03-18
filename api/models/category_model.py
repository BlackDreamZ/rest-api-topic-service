
from api.models import db
# Таблица Категории Товара

class СategoriesProduct(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name_category = db.Column(db.String(), nullable=False)
    products = db.relationship("Product")
    def __repr__(self):
        return "СategoriesProduct {self.name_category}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def toDICT(self):
        cls_dict = {}
        cls_dict['_id'] = self.id
        cls_dict['_name_category'] = self.name_category
        return cls_dict

    def toJSON(self):
        return self.toDICT()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def get_by_name(cls, _name_category):
        return cls.query.filter_by(name_category=_name_category).first()


