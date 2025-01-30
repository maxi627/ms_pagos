from app import cache, db
from app.models import Pagos
from app.repositories import PagosRepository

import logging

# Configuración del logger
logger = logging.getLogger(__name__)

class PagosService:
    """
    Servicio para gestionar pagos con soporte de caché y transacciones seguras.
    """
    def __init__(self, repository=None, cache_helper=None):
        from app.services import CacheHelper
        self.repository = repository or PagosRepository()
        self.cache = cache_helper or CacheHelper(cache)
    
    def all(self) -> list[Pagos]:
        """
        Obtiene todos los pagos con soporte de caché.
        """
        cached_pagos = self.cache.get('pagos')
        if cached_pagos is None:
            pagos = self.repository.get_all()
            if pagos:
                self.cache.set('pagos', pagos)
            return pagos
        return cached_pagos

    def add(self, pago: Pagos) -> Pagos:
        """
        Agrega un nuevo pago con manejo de transacciones y caché.
        """
        try:
            new_pago = self.repository.save(pago)  # Ahora captura el retorno del repositorio
            self.cache.set(f'pagos_{new_pago.id}', new_pago)
            self.cache.delete('pagos')  # Invalida la lista de pagos
            return new_pago
        except Exception as e:
            db.session.rollback()  # Deshacer cualquier cambio en caso de error
            logger.error(f"Error al agregar el pago: {e}")
            raise

    def delete(self, pago_id: int) -> bool:
        """
        Elimina un pago con manejo de transacciones y actualización de caché.
        """
        try:
            deleted = self.repository.delete(pago_id)  # Se pasa el ID en lugar del objeto
            if deleted:
                self.cache.delete(f'pagos_{pago_id}')
                self.cache.delete('pagos')  # Invalida la lista de pagos
            return deleted
        except Exception as e:
            db.session.rollback()  # Rollback si hay error
            logger.error(f"Error al eliminar el pago con ID {pago_id}: {e}")
            raise

    def find(self, pago_id: int) -> Pagos:
        """
        Busca un pago por su ID con soporte de caché.
        """
        cached_pago = self.cache.get(f'pagos_{pago_id}')
        if cached_pago is None:
            pago = self.repository.get_by_id(pago_id)
            if pago:
                self.cache.set(f'pagos_{pago_id}', pago)
            return pago
        return cached_pago
        
    def update(self, pago_id: int, new_data: Pagos) -> Pagos:
        """
        Actualiza un pago existente con nueva información.
    
        :param pago_id: ID del pago a actualizar.
        :param new_data: Objeto Pagos con los nuevos datos.
        :return: Objeto Pagos actualizado.
        """
        try:
            pago = self.repository.get_by_id(pago_id)
            if not pago:
                return None  # El controlador manejará el 404
    
            # Actualizar solo los campos que vienen en `new_data`
            for key, value in new_data.__dict__.items():
                if value is not None:  # Evita sobreescribir con `None`
                    setattr(pago, key, value)
    
            updated_pago = self.repository.save(pago)
            self.cache.set(f'pagos_{pago.id}', updated_pago)
            self.cache.delete('pagos')  # Invalida la lista de pagos en caché
            return updated_pago
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al actualizar el pago con ID {pago_id}: {e}")
            raise
