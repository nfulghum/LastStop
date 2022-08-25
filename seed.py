

from app import app
from models import db, User

db.drop_all()
db.create_all()

u1 = User(
    name="Nick",
    email="nick@gmail.com",
    phone=222-222-2222,
    username="CampingGuy",
    city="Houston",
    state="TX",
    zip=77055
)
