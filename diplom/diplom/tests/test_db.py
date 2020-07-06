from .. import vkinder_db.db_functionality as db_func
from .. import vkinder_user

import unittest


class VkinderTester(unittest.TestCase):
    def test_user_existent(self):
        test_user = vkinder_user.VKinderUser(user_id=123, token=0, name='Test_name', age=18,
                                             sex=2, city=3, status=6)
        self.assertIsNotNone(db_func.VKinderDB.add_user(test_user))

        self.assertTrue(db_func.VKinderDB.get_existent_user)

    def test_suggestion_counter(self):
        current_ctr = db_func.VKinderDB.count_suggestions()
        for i in range(16):
            new_user = vkinder_user.VKinderUser(user_id=i)
            new_user.photos = [f'some_url_{i}_j' for j in range(3)]
            db_func.VKinderDB.add_suggestion(**new_user.get_dict())

        new_ctr = db_func.VKinderDB.count_suggestions()
        self.assertEqual(new_ctr, current_ctr + 16)


if __name__ == '__main__':
    unittest.main()
