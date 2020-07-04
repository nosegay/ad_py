from .. import vkinder_user

import unittest


class VkinderTester(unittest.TestCase):
    def test_id_getter(self):
        test_user = vkinder_user.VKinderUser('eshmargunov', '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008')
        self.assertEqual(test_user.id, 171691064)

if __name__ == '__main__':
    unittest.main()
