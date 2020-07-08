from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from vkinder_db.init_db import create_all, VKinderUsers, VKinderSuggestions


class VKinderDB:
    def __init__(self, db_name, db_user, db_user_pwd):
        engine = create_engine('postgresql+psycopg2://%s:%s@localhost/%s' % (db_user, db_user_pwd, db_name))
        Session = sessionmaker(bind=engine)
        self.session = Session()
        create_all(engine)

    def add_user(self, user):
        vkinder_user = VKinderUsers(name=user.name, age=user.age, sex=user.sex, city=user.city, status=user.status,
                                    vk_id=str(user))
        self.session.add(vkinder_user)
        self.session.commit()
        return vkinder_user.id

    def add_suggestion(self, main_id, **user):
        vkinder_pair = VKinderSuggestions(user_id=main_id, partner_vk_id=user['vk_user'], photos_1=user['photos'][0],
                                          photos_2=user['photos'][1], photos_3=user['photos'][2])
        self.session.add(vkinder_pair)
        self.session.commit()

    def get_existent_user(self, user):
        result = self.session.query(VKinderUsers).filter(VKinderUsers.vk_id == str(user)).first()
        if result is not None:
            user.name = result.name
            user.age = result.age
            user.sex = result.sex
            user.city = result.city
            user.status = result.status
            return True
        return False

    def count_suggestions(self, user_id):
        return self.session.query(VKinderSuggestions).filter(VKinderSuggestions.user_id == user_id).count()
