from models.ClientType import ClientType


class ClientTypeService():
    def __init__(self) -> None:
        self.ClientTypeModel = ClientType

    def create(self, title):
        return self.ClientTypeModel.create(title=title)

    def update(self, id: int, title: str):
        self.ClientTypeModel.update({self.ClientTypeModel.title: title}).where(
            self.ClientTypeModel.id == id).execute()

    def delete(self, id: int):
        self.ClientTypeModel = self.ClientTypeModel.get_by_id(id)
        self.ClientTypeModel.delete_instance(recursive=True)

    def get_all(self):
        return [client_type for client_type in self.ClientTypeModel.select()]
