from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import ServiceTicket, Mechanic, db
from . import service_tickets_bp
from app.blueprints.mechanics.schemas import mechanic_schema
from app.utils.util import token_required


@service_tickets_bp.route('/', methods=['POST'])
def create_service_ticket():
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_service_ticket = ServiceTicket(**service_ticket_data)
    db.session.add(new_service_ticket)
    db.session.commit()

    return service_ticket_schema.jsonify(new_service_ticket), 201

@service_tickets_bp.route('/', methods=['GET'])
def get_service_tickets():
    query = select(ServiceTicket)
    service_tickets = db.session.scalars(query).all()
    return service_tickets_schema.jsonify(service_tickets), 200

@service_tickets_bp.route('/<ticket_id>/assign-mechanic/<mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    service_ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)
    if service_ticket and mechanic:
        if mechanic not in service_ticket.mechanics:
            service_ticket.mechanics.append(mechanic)
            db.session.commit()
            return jsonify({
                "message": "successfully assigned mechanic to service ticket",
                "service_ticket": service_ticket_schema.dump(service_ticket),
                "mechanic": mechanic_schema.dump(mechanic)
            }), 200
        return jsonify({"error": "Mechanic already assigned to this service ticket"}), 400
    return jsonify({"error": "Service ticket or mechanic not found"}), 404

@service_tickets_bp.route('/<ticket_id>/remove-mechanic/<mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    service_ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if service_ticket and mechanic:
        if mechanic in service_ticket.mechanics:
            service_ticket.mechanics.remove(mechanic)
            db.session.commit()
            return jsonify({
                "message": "successfully removed mechanic from service ticket",
                "service_ticket": service_ticket_schema.dump(service_ticket),
                "mechanic": mechanic_schema.dump(mechanic)
            }), 200
        return jsonify({"error": "Mechanic not assigned to this service ticket"}), 400
    return jsonify({"error": "Service ticket or mechanic not found"}), 404


@service_tickets_bp.route('/my-tickets', methods=['GET']) # Endpoint becomes /loans/mine
@token_required
def get_my_service_tickets(customer_id):
    # token_id is passed from the decorator
    query = select(ServiceTicket).where(ServiceTicket.customer_id == customer_id)
    service_tickets = db.session.execute(query).scalars().all()

    return service_tickets_schema.jsonify(service_tickets), 200