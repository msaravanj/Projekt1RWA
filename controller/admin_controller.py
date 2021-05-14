from flask_restplus import Namespace, Resource, fields
from model._init_ import db
from model.user import User
from model.event import Event
from service.auth_service import admin_only
from controller.user_controller import user_dto
from controller.event_controller import event_dto

api = Namespace(name='Admin API', path='/api/admin')

@api.route('/db/init-db')
class DatabaseResource(Resource):
    @api.doc(description='Initialize database', security='Admin Auth', responses={200: 'Success', 401: 'Not Authorized', 403: 'Forbidden'})
    @admin_only
    def post(self):
        db.create_all()
        return {'message': 'Database initialization complete.'}


@api.route('/u/<email>')
@api.param('email', 'User email address')
@api.response(404, 'User not found.')
class UserResource(Resource):
    @api.doc(description='Get a user', responses={200: 'Success', 403: 'Forbidden'}, security='Admin Auth')
    @api.marshal_with(user_dto)
    def get(self, email):
        user = User.query.filter_by(email=email).first()
        if not user:
            api.abort(404)
        else:
            return user 

    @api.doc(description='Delete a user', responses={200: 'Success', 403: 'Forbidden'}, security='Admin Auth')
    def delete(self, email):
        user = User.query.filter_by(email=email).first()
        if not user:
            api.abort(404)
        else:
            db.session.delete(user)
            db.session.commit()
            return {'message' : 'The user has been deleted!'}

@api.route('/u/<email>/promote')
@api.param('email', 'User email address')
@api.response(404, 'User not found.')
class UserPromoteResource(Resource):
    @api.doc(description='Promote a user to Admin', responses={200: 'Success', 403: 'Forbidden'}, security='Admin Auth')
    def post(self, email):
        user = User.query.filter_by(email=email).first()
        if not user:
            api.abort(404)
        else:
            user.admin = True
            db.session.commit()
            return {'message' : 'The user has been promoted!'}

@api.route('/u')
class UserListResource(Resource):
    @api.doc(description='Get all users', responses={200: 'Success', 403: 'Forbidden'}, security='Admin Auth')
    @api.marshal_list_with(user_dto)
    @admin_only
    def get(self):
        users = User.query.all()

        output = []

        for user in users:
            user_data = {}
            user_data['email'] = user.email
            user_data['first_name'] = user.first_name
            user_data['last_name'] = user.last_name
            user_data['password'] = user.password
            user_data['admin'] = user.admin
            user_data['created'] = user.created
            user_data['updated'] = user.updated
            output.append(user_data)

        return output                     


@api.route('/events')
class EventListResource(Resource):
    @api.doc(description='Get all events', responses={200: 'Success', 403: 'Forbidden'}, security='Admin Auth')
    @api.marshal_list_with(event_dto)
    @admin_only
    def get(self):
        events = Event.query.all()

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


    @api.route('/events/<id>')
    @api.param('id', 'Event ID')
    @api.response(404, 'Event not found.')
    class EventDeleteResource(Resource):
        @api.doc(description='Delete an event', responses={200: 'Success', 403: 'Forbidden'}, security='Admin Auth')
        def delete(self, id):
            event = Event.query.filter_by(id=id).first()
            if not event:
                api.abort(404)
            else:
                db.session.delete(event)
                db.session.commit()
                return {'message' : 'The event has been deleted!'}