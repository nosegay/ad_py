from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from vkinder_db.init_db import create_all, VKinderUsers, VKinderSuggestions


class VKinderDB:
    engine = create_engine('postgresql+psycopg2://vkinder_db_user:test123@localhost/vkinder_db')
    Session = sessionmaker(bind=engine)
    session = Session()
    create_all(engine)

    @staticmethod
    def add_user(user):
        vkinder_user = VKinderUsers(name=user.name, age=user.age, sex=user.sex, city=user.city, status=user.status,
                                    vk_id=str(user))
        VKinderDB.session.add(vkinder_user)
        VKinderDB.session.commit()
        return vkinder_user.id

    @staticmethod
    def add_suggestion(**user):
        vkinder_pair = VKinderSuggestions(vk_id=user['vk_user'], photos_1=user['photos'][0], photos_2=user['photos'][1],
                                          photos_3=user['photos'][2])
        VKinderDB.session.add(vkinder_pair)
        VKinderDB.session.commit()

    @staticmethod
    def get_existent_user(user):
        result = VKinderDB.session.query(VKinderUsers).first()
        if result is not None:
            user.name = result.name
            user.age = result.age
            user.sex = result.sex
            user.city = result.city
            user.status = result.status
            return True
        return False

    @staticmethod
    def count_suggestions():
        return VKinderDB.session.query(VKinderSuggestions).count()
