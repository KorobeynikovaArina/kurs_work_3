from models.ClientType import ClientType
import shutil


class ClientTypeService():
    def __init__(self) -> None:
        self.ClientTypeModel = ClientType

    def create(self, title):
        return self.ClientTypeModel.create(title=title)

    def update(self, id: int, title: str):
        self.ClientTypeModel.update({self.ClientTypeModel.title: title}).where(
            self.ClientTypeModel.id == id).execute()

    def delete(self, id: int):
        client_type = self.ClientTypeModel.get_by_id(id)
        shutil.rmtree(client_type.upload_dir)
        client_type.delete_instance(recursive=True)

    def get_all(self):
        return [client_type for client_type in self.ClientTypeModel.select()]

    def get_by_id(self, id: int):
        return self.ClientTypeModel.get_by_id(id)
