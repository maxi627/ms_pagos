from app import cache
from app.models import Pagos
from app.repositories import PagosRepository
from app.services import CacheHelper
import logging

# Configuración del logger
logger = logging.getLogger(__name__)

class PagosService:
    """
    Servicio para gestionar pagos con soporte de caché.
    """
    def __init__(self, repository=None, cache_helper=None):
        """
        Inicializa el servicio de pagos.

        :param repository: Repositorio para operaciones con la base de datos.
        :param cache_helper: Instancia de CacheHelper para manejar caché.
        """
        self.repository = repository or PagosRepository()
        self.cache = cache_helper or CacheHelper(cache)

    def all(self) -> list[Pagos]:
        """
        Obtiene todos los pagos. Usa caché para optimizar rendimiento.

        :return: Lista de objetos Pagos.
        """
        cached_pagos = self.cache.get('pagos')
        if cached_pagos is None:
            pagos = self.repository.get_all()
            if pagos:
                self.cache.set('pagos', pagos)
            return pagos
        return cached_pagos

    def add(self, pagos: Pagos) -> Pagos:
        """
        Agrega un nuevo pago, actualiza la base de datos y la caché.

        :param pagos: Objeto Pagos a agregar.
        :return: Objeto Pagos recién creado.
        """
        try:
            new_pago = self.repository.save(pagos)
            self.cache.set(f'pagos_{new_pago.id}', new_pago)
            self.cache.delete('pagos')
            return new_pago
        except Exception as e:
            logger.error(f"Error al agregar el pago: {e}")
            raise

    def delete(self, pago_id: int) -> bool:
        """
        Elimina un pago por su ID. Invalida la caché correspondiente.

        :param pago_id: ID del pago a eliminar.
        :return: True si se eliminó correctamente, False en caso contrario.
        """
        try:
            deleted = self.repository.delete(pago_id)
            if deleted:
                self.cache.delete(f'pagos_{pago_id}')
                self.cache.delete('pagos')  # Invalida la lista de pagos
            return deleted
        except Exception as e:
            logger.error(f"Error al eliminar el pago con ID {pago_id}: {e}")
            raise

    def find(self, pago_id: int) -> Pagos:
        """
        Busca un pago por su ID. Usa caché para optimizar.

        :param pago_id: ID del pago a buscar.
        :return: Objeto Pagos si se encuentra, None si no existe.
        """
        cached_pago = self.cache.get(f'pagos_{pago_id}')
        if cached_pago is None:
            pago = self.repository.get_by_id(pago_id)
            if pago:
                self.cache.set(f'pagos_{pago_id}', pago)
            return pago
        return cached_pago
