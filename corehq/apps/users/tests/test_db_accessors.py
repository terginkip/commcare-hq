from django.test import TestCase
from corehq.apps.users.models import WebUser, CommCareUser
from corehq.apps.users.dbaccessors.all_commcare_users import (
    get_all_commcare_users_by_domain,
    get_user_docs_by_username,
    delete_all_users,
    get_all_user_ids,
    get_deleted_user_by_username,
)
from corehq.apps.users.dbaccessors.couch_users import (
    get_user_id_by_username,
)
from corehq.apps.domain.models import Domain
from corehq.apps.users.dbaccessors.all_commcare_users import hard_delete_deleted_users


class AllCommCareUsersTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(AllCommCareUsersTest, cls).setUpClass()
        delete_all_users()
        hard_delete_deleted_users()
        cls.ccdomain = Domain(name='cc_user_domain')
        cls.ccdomain.save()
        cls.other_domain = Domain(name='other_domain')
        cls.other_domain.save()

        cls.ccuser_1 = CommCareUser.create(
            domain=cls.ccdomain.name,
            username='ccuser_1',
            password='secret',
            email='email@example.com',
        )
        cls.ccuser_2 = CommCareUser.create(
            domain=cls.ccdomain.name,
            username='ccuser_2',
            password='secret',
            email='email1@example.com',
        )
        cls.web_user = WebUser.create(
            domain=cls.ccdomain.name,
            username='webuser',
            password='secret',
            email='webuser@example.com',
        )
        cls.ccuser_other_domain = CommCareUser.create(
            domain=cls.other_domain.name,
            username='cc_user_other_domain',
            password='secret',
            email='email_other_domain@example.com',
        )
        cls.retired_user = CommCareUser.create(
            domain=cls.ccdomain.name,
            username='retired_user',
            password='secret',
            email='retired_user_email@example.com',
        )
        cls.retired_user.retire()

    @classmethod
    def tearDownClass(cls):
        delete_all_users()
        super(AllCommCareUsersTest, cls).tearDownClass()

    def test_get_all_commcare_users_by_domain(self):
        expected_users = [self.ccuser_2, self.ccuser_1]
        expected_usernames = [user.username for user in expected_users]
        actual_usernames = [user.username for user in get_all_commcare_users_by_domain(self.ccdomain.name)]
        self.assertItemsEqual(actual_usernames, expected_usernames)

    def test_exclude_retired_users(self):
        deleted_user = CommCareUser.create(
            domain=self.ccdomain.name,
            username='deleted_user',
            password='secret',
            email='deleted_email@example.com',
        )
        deleted_user.retire()
        self.assertNotIn(
            deleted_user.username,
            [user.username for user in
             get_all_commcare_users_by_domain(self.ccdomain.name)]
        )
        deleted_user.delete()

    def test_get_user_docs_by_username(self):
        users = [self.ccuser_1, self.web_user, self.ccuser_other_domain]
        usernames = [u.username for u in users] + ['nonexistant@username.com']
        self.assertItemsEqual(
            get_user_docs_by_username(usernames),
            [u.to_json() for u in users]
        )

    def test_get_all_ids(self):
        all_ids = get_all_user_ids()
        self.assertEqual(4, len(all_ids))
        for id in [self.ccuser_1._id, self.ccuser_2._id, self.web_user._id, self.ccuser_other_domain._id]:
            self.assertTrue(id in all_ids)

    def test_get_id_by_username(self):
        user_id = get_user_id_by_username(self.ccuser_1.username)
        self.assertEqual(user_id, self.ccuser_1._id)

    def test_get_deleted_user_by_username(self):
        self.assertEqual(self.retired_user['_id'],
                         get_deleted_user_by_username(CommCareUser, self.retired_user.username)['_id'])
        self.assertEqual(None, get_deleted_user_by_username(CommCareUser, self.ccuser_2.username))
