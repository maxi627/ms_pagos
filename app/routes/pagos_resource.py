from flask import Blueprint, request
from marshmallow import ValidationError
from app.mapping import PagosSchema, ResponseSchema
from app.services import PagosService, ResponseBuilder

Pagos = Blueprint('Pagos', __name__)  
service = PagosService()
pagos_schema = PagosSchema()
response_schema = ResponseSchema()

@Pagos.route('/pagos', methods=['GET'])  
def all():
    response_builder = ResponseBuilder()
    try:
        data = pagos_schema.dump(service.all(), many=True)
        response_builder.add_message("Pagos found").add_status_code(200).add_data(data)
        return response_schema.dump(response_builder.build()), 200
    except Exception as e:
        response_builder.add_message("Error fetching pagos").add_status_code(500).add_data(str(e))
        return response_schema.dump(response_builder.build()), 500

@Pagos.route('/pagos/<int:id>', methods=['GET'])  
def one(id):
    response_builder = ResponseBuilder()
    try:
        data = service.find(id)
        if data:
            serialized_data = pagos_schema.dump(data)
            response_builder.add_message("Pago found").add_status_code(200).add_data(serialized_data)
            return response_schema.dump(response_builder.build()), 200
        else:
            response_builder.add_message("Pago not found").add_status_code(404).add_data({'id': id})
            return response_schema.dump(response_builder.build()), 404
    except Exception as e:
        response_builder.add_message("Error fetching pago").add_status_code(500).add_data(str(e))
        return response_schema.dump(response_builder.build()), 500

@Pagos.route('/pagos', methods=['POST'])  
def add():
    response_builder = ResponseBuilder()
    try:
        json_data = request.json
        if not json_data:
            raise ValidationError("No data provided")
        
        pago = pagos_schema.load(json_data)
        data = pagos_schema.dump(service.add(pago))
        response_builder.add_message("Pago created").add_status_code(201).add_data(data)
        return response_schema.dump(response_builder.build()), 201
    except ValidationError as err:
        response_builder.add_message("Validation error").add_status_code(422).add_data(err.messages)
        return response_schema.dump(response_builder.build()), 422
    except Exception as e:
        response_builder.add_message("Error creating pago").add_status_code(500).add_data(str(e))
        return response_schema.dump(response_builder.build()), 500

@Pagos.route('/pagos/<int:id>', methods=['PUT'])
def update(id):
    response_builder = ResponseBuilder()
    try:
        json_data = request.json
        if not json_data:
            raise ValidationError("No data provided")
        
        pago = pagos_schema.load(json_data)
        updated_pago = service.update(id, pago)
        if not updated_pago:
            response_builder.add_message("Pago not found").add_status_code(404).add_data({'id': id})
            return response_schema.dump(response_builder.build()), 404
        
        data = pagos_schema.dump(updated_pago)
        response_builder.add_message("Pago updated").add_status_code(200).add_data(data)
        return response_schema.dump(response_builder.build()), 200
    except ValidationError as err:
        response_builder.add_message("Validation error").add_status_code(422).add_data(err.messages)
        return response_schema.dump(response_builder.build()), 422
    except Exception as e:
        response_builder.add_message("Error updating pago").add_status_code(500).add_data(str(e))
        return response_schema.dump(response_schema.build()), 500

@Pagos.route('/pagos/<int:id>', methods=['DELETE'])
def delete(id):
    response_builder = ResponseBuilder()
    try:
        if service.delete(id):
            response_builder.add_message("Pago deleted").add_status_code(200).add_data({'id': id})
            return response_schema.dump(response_builder.build()), 200
        else:
            response_builder.add_message("Pago not found").add_status_code(404).add_data({'id': id})
            return response_schema.dump(response_builder.build()), 404
    except Exception as e:
        response_builder.add_message("Error deleting pago").add_status_code(500).add_data(str(e))
        return response_schema.dump(response_builder.build()), 500
