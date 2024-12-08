from flask import Blueprint, jsonify, request

from app.mapping import PagosSchema
from app.services import PagosService

Pagos = Blueprint('Pagos', __name__)
service = PagosService()
Pagos_schema =PagosSchema()

"""
Obtiene todos las Pagos
"""
@Pagos.route('/Pagos', methods=['GET'])
def all():
    resp = Pagos_schema.dump(service.get_all(), many=True) 
    return resp, 200

"""
Obtiene una Pagos por id
"""
@Pagos.route('/Pagos/<int:id>', methods=['GET'])
def one(id):
    resp = Pagos_schema.dump(service.get_by_id(id)) 
    return resp, 200

"""
Crea nueva Pagos
"""
@Pagos.route('/Pagos', methods=['POST'])
def create():
    Pagos = Pagos_schema.load(request.json)
    resp = Pagos_schema.dump(service.create(Pagos))
    return resp, 201

"""
Actualiza una Pagos existente
"""
@Pagos.route('/Pagos/<int:id>', methods=['PUT'])
def update(id):
    Pagos = Pagos_schema.load(request.json)
    resp = Pagos_schema.dump(service.update(id, Pagos))
    return resp, 200

"""
Elimina una Pagos existente
"""
@Pagos.route('/Pagos/<int:id>', methods=['DELETE'])
def delete(id):
    msg = "Pagos eliminado correctamente"
    resp = service.delete(id)
    if not resp:
        msg = "No se pudo eliminar el Pagos"
    return jsonify(msg), 204