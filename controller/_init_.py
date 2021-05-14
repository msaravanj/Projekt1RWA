from flask_restplus import Api

from .auth_controller import api as auth_ns
from .user_controller import api as user_ns
from .admin_controller import api as admin_ns
from .event_controller import api as event_ns

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
    'Basic Auth': {
        'type': 'basic',
        'in': 'header',
        'name': 'Authorization'
    },
    'Admin Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-Admin-Token'
    }
}

api = Api(
    title='Event API',
    version='1.0.0',
    description='Sveučilište u Zadru - Studij informacijske tehnologije - Razvoj web aplikacija \nProjekt 1',
    contact='sarosaravanja11@gmail.com',
    authorizations=authorizations,
    serve_challenge_on_401=False
)

api.add_namespace(auth_ns)
api.add_namespace(user_ns)
api.add_namespace(admin_ns)
api.add_namespace(event_ns)