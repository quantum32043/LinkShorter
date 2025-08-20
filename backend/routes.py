from fastapi import APIRouter

routes = APIRouter(prefix="/api")

@routes.post('/login')
def login(email, password):
    pass


@routes.post('/logout')
def logout():
    pass


@routes.post('/register')
def register(email, password):
    pass


@routes.post('/refresh')
def refresh():
    pass
