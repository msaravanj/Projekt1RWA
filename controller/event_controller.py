from flask import request, jsonify
from flask_restplus import Namespace, Resource, fields
from werkzeug import security
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from model._init_ import db
from model.event import Event
from service.auth_service import authenticated, authenticated_admin
from service.log_service import trace

api = Namespace(name='Event API', path='/api/events', decorators=[trace])

event_create_dto = api.model('CreateEvent', {
    'title': fields.String(required=True, description='Title'),
    'date': fields.String(required=True, description='Date'),
    'location': fields.String(required=True, description='Location'),
    'price': fields.Integer(required=True, description='Price'),
    
})

event_dto = api.model('Event', {
    'id': fields.Integer(required=True, description='ID'),
    'title': fields.String(required=True, description='Title'),
    'date': fields.String(required=True, description='Date'),
    'location': fields.String(required=True, description='Location'),
    'price': fields.Integer(required=True, description='Price'),
    'complete': fields.Boolean(required=True, description='Complete'),
    'user_id': fields.Integer(required=True, description='User ID'),
    'created': fields.DateTime(required=True, description='Created'),
    'updated': fields.DateTime(required=True, description='Updated')
})

event_update_dto = api.model('UpdateEvent', {
    'date': fields.String(required=False, description="Date"),
    'location': fields.String(required=False, description='Location'),
    'price': fields.String(required=False, description='Price')
})


@api.route('/')
class EventListResource(Resource):
  
    @api.doc(description='Create an event', responses={201: 'Success', 401: 'Unauthorized'}, security='Bearer Auth')
    @api.expect(event_create_dto)
    @api.marshal_with(event_dto)
    @authenticated
    def post(current_user,self):
      
        new_event = Event(title=api.payload['title'], date=api.payload['date'], location=api.payload['location'], price=api.payload['price'], complete=False, user_id=current_user.id)
        db.session.add(new_event)
        db.session.commit()
        
        return new_event, 201

    @api.doc(description='Get my events', responses={200: 'Success', 403: 'Forbidden'}, security='Bearer Auth')
    @api.marshal_list_with(event_dto)
    @authenticated
    def get(current_user, self):
        
        events = Event.query.filter_by(user_id=current_user.id)
    
        output = []

        for event in events:
            event_data = {}
            event_data['id'] = event.id
            event_data['title'] = event.title
            event_data['date'] = event.date
            event_data['location'] = event.location
            event_data['price'] = event.price
            event_data['complete'] = event.complete
            event_data['user_id'] = event.user_id            
            event_data['created'] = event.created
            event_data['updated'] = event.updated
            output.append(event_data)

        return output         


@api.route('/<id>')
@api.param('id', 'ID')
@api.response(404, 'Event not found.')
class EventResource(Resource):
    @api.doc(description='Get an event', responses={200: 'Success', 403: 'Forbidden'}, security='Bearer Auth')
    @api.marshal_with(event_dto)
    @authenticated
    def get(current_user, self, id):
        event = Event.query.filter_by(id=id, user_id=current_user.id).first()
        if not event:
            api.abort(404)
        else:
            return event  


    @api.doc(description='Update an event', responses={200: 'Success', 403: 'Forbidden'}, security='Bearer Auth')
    @api.expect(event_update_dto)
    @authenticated
    def put(current_user, self, id):
        event = Event.query.filter_by(id=id, user_id=current_user.id).first()
        if not event.id:
            api.abort(404)
        else:
            if 'price' in api.payload:
                event.price = api.payload['price']
            if 'location' in api.payload:
                event.location = api.payload['location']
            if 'date' in api.payload: 
                event.date = api.payload['date']
            
            db.session.commit()
            return {'message': 'Event successfully updated!'}



    @api.doc(description='Delete an event', responses={200: 'Success', 403: 'Forbidden'}, security='Bearer Auth')
    @authenticated
    def delete(current_user, self, id):
        event = Event.query.filter_by(id=id, user_id=current_user.id).first()
        if not event:
            api.abort(404)
        else:
            db.session.delete(event)
            db.session.commit()
            return {'message': 'Event has been deleted'}    


@api.route('/<id>/complete')
@api.param('id', 'ID')
@api.response(404, 'Event not found.')
class EventCompleteResource(Resource):
    @api.doc(description='Complete an event', responses={200: 'Success', 403: 'Forbidden'}, security='Bearer Auth')
    @api.marshal_with(event_dto)
    @api.param('complete', description='Complete', type='boolean')
    @authenticated
    def put(current_user, self, id):
        event = Event.query.filter_by(id=id, user_id=current_user.id).first()
        if not event:
            api.abort(404)
        else:
            complete = request.args.get('complete')

            if complete == 'true':
                event.complete = True
            elif complete == 'false':
                event.complete = False

            db.session.commit()
            return event          
