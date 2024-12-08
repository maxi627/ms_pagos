from typing import List

from app import db
from app.models import Pagos

from .repository import Repository_delete, Repository_get, Repository_save


class PagosRepository(Repository_save, Repository_get, Repository_delete):
    def save(self, entity: Pagos) -> Pagos:
        db.session.add(entity)
        db.session.commit()
        return entity

    def get_all(self) -> List[Pagos]:
        return Pagos.query.all()

    def get_by_id(self, id: int) -> Pagos:
        return Pagos.query.get(id)

    def delete(self, id: int) -> bool:
        Pagos = self.get_by_id(id)
        if Pagos:
            db.session.delete(Pagos)
            db.session.commit()
            return True
        return False
