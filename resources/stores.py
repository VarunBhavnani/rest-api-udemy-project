
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schema import StoreSchema
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from db import db
from Models import StoreModel


blp = Blueprint("Stores", "stores", description="Operations on stores")


@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200,StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message":"store deleted"}


@blp.route("/store")
class StoreList(MethodView):
    
    @blp.response(201,StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self,store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message = "An error occured while inserting item to db")

        return store