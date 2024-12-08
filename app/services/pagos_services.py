from app import cache
from app.models import Pagos
from app.repositories import PagosRepository

repository = PagosRepository()

class PagosService:
    def all(self) -> list[Pagos]:
        result = cache.get('pagos')
        if result is None:
            result = repository.get_all()
            if result:
                cache.set('pagos', result, timeout=60)  # Considera un timeout más largo
        return result

    def add(self, pagos: Pagos) -> Pagos:
        pagos = repository.save(pagos)
        cache.set(f'pagos_{pagos.id}', pagos, timeout=60)
        cache.delete('pagos')  # Invalida la lista de pagos
        return pagos

    def delete(self, id: int) -> bool:
        result = repository.delete(id)
        if result:
            cache.delete(f'pagos_{id}')
            cache.delete('pagos')  # Invalida la lista de pagos
        return result

    def find(self, id: int) -> Pagos:
        result = cache.get(f'pagos_{id}')
        if result is None:
            result = repository.get_by_id(id)
            if result:
                cache.set(f'pagos_{id}', result, timeout=60)
        return result
