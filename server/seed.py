from app import db, User

def seed_database():
    db.create_all()

    # Create test users
    user1 = User(username="Mohammed Salah")
    user1.set_password("password123")

    user2 = User(username="Cody Gakpo")
    user2.set_password("secret456")

    db.session.add_all([user1, user2])
    db.session.commit()

if __name__ == "__main__":
    seed_database()

