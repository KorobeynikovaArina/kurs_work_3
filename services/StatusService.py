from models.Status import Status


class StatusService():
    def __init__(self) -> None:
        self.StatusModel = Status

    def create(self, title: str):
        return self.StatusModel.create(title=title)

    def update(self, id: int, title: str):
        self.StatusModel.update({self.StatusModel.title: title}).where(
            self.StatusModel.id == id).execute()

    def delete(self, id: int):
        status = self.StatusModel.get_by_id(id)
        status.delete_instance(recursive=True)

    def get_all(self):
        return [status for status in self.StatusModel.select()]

    def get_by_id(self, id: int):
        return self.StatusModel.get_by_id(id)
