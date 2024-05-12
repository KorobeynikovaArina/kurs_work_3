import os
from models.ClientType import ClientType
from models.Order import Order
from models.Status import Status
from models.User import User


class OrderService():
    def __init__(self) -> None:
        self.OrderModel = Order

    def create(self, client: str, client_type: ClientType, contact, product_type, material_filepath, user: User, status: Status):
        return self.OrderModel.create(client=client,
                                      client_type=client_type,
                                      contact=contact,
                                      product_type=product_type,
                                      material_filepath=material_filepath,
                                      user=user,
                                      status=status)

    def update(self, id: int, *args, **kwargs):

        client = kwargs.get("client", None)
        client_type = kwargs.get("client_type", None)
        contact = kwargs.get("contact", None)
        product_type = kwargs.get("product_type", None)
        material_filepatht = kwargs.get("material_filepatht", None)
        user = kwargs.get("user", None)
        status = kwargs.get("status", None)

        order = {}

        if client:
            order[self.OrderModel.client] = client
        if client_type:
            order[self.OrderModel.client_type] = client_type
        if contact:
            order[self.OrderModel.contact] = contact
        if product_type:
            order[self.OrderModel.product_type] = product_type
        if material_filepatht:
            order[self.OrderModel.material_filepath] = material_filepatht
        if user:
            order[self.OrderModel.user] = user
        if status:
            order[self.OrderModel.status] = status

        self.OrderModel.update(order).where(self.OrderModel.id == id).execute()

    def delete(self, id: int):
        order = self.OrderModel.get_by_id(id)

        files = order.materials.split(',')

        for f in files:
            os.remove(f)

        order.delete_instance()

    def get_by_id(self, id: int):
        return self.OrderModel.get_by_id(id)

    def get_all(self):
        return [order for order in self.OrderModel.select()]
