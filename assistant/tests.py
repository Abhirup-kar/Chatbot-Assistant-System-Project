import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .management.commands.seed_kb import ensure_knowledge_base_seeded
from .models import ChatMessage, TechGuide, UserProfile


class ChatbotAssistantTests(TestCase):
    def setUp(self):
        ensure_knowledge_base_seeded()
        self.user_password = 'StrongPass!123'
        self.user = User.objects.create_user(
            username='alice',
            first_name='Alice',
            last_name='Dev',
            email='alice@example.com',
            password=self.user_password,
        )
        UserProfile.objects.create(
            user=self.user,
            phone='555-0100',
            occupation='Developer',
            address='123 Python Ave',
        )

    def test_seed_kb_is_idempotent(self):
        initial_count = TechGuide.objects.count()
        self.assertGreaterEqual(initial_count, 16)
        created, updated = ensure_knowledge_base_seeded()
        self.assertEqual(created, 0)
        self.assertEqual(updated, initial_count)
        self.assertEqual(TechGuide.objects.count(), initial_count)

    def test_registration_creates_user_and_profile(self):
        response = self.client.post(
            reverse('assistant:register'),
            {
                'username': 'bob_user',
                'first_name': 'Bob',
                'last_name': 'Tester',
                'email': 'bob@example.com',
                'phone': '555-0199',
                'occupation': 'Student',
                'address': '42 Django St',
                'password1': 'ComplexPass!99',
                'password2': 'ComplexPass!99',
            },
        )
        self.assertRedirects(response, reverse('assistant:login'))
        new_user = User.objects.get(username='bob_user')
        self.assertEqual(new_user.first_name, 'Bob')
        self.assertEqual(new_user.email, 'bob@example.com')
        self.assertEqual(new_user.profile.phone, '555-0199')
        self.assertEqual(new_user.profile.occupation, 'Student')

    def test_registration_rejects_duplicate_username(self):
        response = self.client.post(
            reverse('assistant:register'),
            {
                'username': 'alice',
                'first_name': 'Dup',
                'last_name': 'User',
                'email': 'dup@example.com',
                'password1': 'ComplexPass!99',
                'password2': 'ComplexPass!99',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(username='alice').count(), 1)

    def test_anonymous_access_redirects_on_protected_routes(self):
        protected_urls = [
            reverse('assistant:chat'),
            reverse('assistant:edit_profile'),
            reverse('assistant:guide_list'),
            reverse('assistant:guide_detail', kwargs={'slug': 'django-project-setup'}),
            reverse('assistant:chat_api'),
        ]
        for url in protected_urls:
            if url == reverse('assistant:chat_api'):
                resp = self.client.post(url, data=json.dumps({'message': 'hi'}), content_type='application/json')
            else:
                resp = self.client.get(url)
            self.assertEqual(resp.status_code, 302)
            self.assertIn(reverse('assistant:login'), resp['Location'])

    def test_login_and_logout_flow(self):
        login_resp = self.client.post(
            reverse('assistant:login'),
            {'username': 'alice', 'password': self.user_password},
        )
        self.assertRedirects(login_resp, reverse('assistant:chat'))

        logout_resp = self.client.post(reverse('assistant:logout'))
        self.assertRedirects(logout_resp, reverse('assistant:login'))

    def test_edit_user_details_and_password_change(self):
        self.client.login(username='alice', password=self.user_password)

        # Edit profile details
        resp = self.client.post(
            reverse('assistant:edit_profile'),
            {
                'form_type': 'profile',
                'first_name': 'Alicia',
                'last_name': 'Engineer',
                'email': 'alicia@example.com',
                'phone': '555-8888',
                'occupation': 'Backend Engineer',
                'address': '99 Cloud Way',
                'bio': 'Python & Django enthusiast',
            },
        )
        self.assertRedirects(resp, reverse('assistant:edit_profile'))
        self.user.refresh_from_db()
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Alicia')
        self.assertEqual(self.user.email, 'alicia@example.com')
        self.assertEqual(self.user.profile.phone, '555-8888')
        self.assertEqual(self.user.profile.bio, 'Python & Django enthusiast')

        # Change password
        new_pw = 'BrandNewPass!456'
        pw_resp = self.client.post(
            reverse('assistant:edit_profile'),
            {
                'form_type': 'password',
                'old_password': self.user_password,
                'new_password1': new_pw,
                'new_password2': new_pw,
            },
        )
        self.assertRedirects(pw_resp, reverse('assistant:edit_profile'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_pw))

    def _post_chat(self, message: str):
        return self.client.post(
            reverse('assistant:chat_api'),
            data=json.dumps({'message': message}),
            content_type='application/json',
        )

    def test_chatbot_setup_and_troubleshooting_queries_with_clickable_links(self):
        self.client.login(username='alice', password=self.user_password)

        # 1. Django setup query -> returns internal guide link + navigates cleanly
        resp = self._post_chat('how to setup django')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        bot_links = data['bot_message']['links']
        internal_links = [lnk for lnk in bot_links if lnk['type'] == 'internal']
        self.assertTrue(any('django-project-setup' in lnk['url'] for lnk in internal_links))

        guide_resp = self.client.get(internal_links[0]['url'])
        self.assertEqual(guide_resp.status_code, 200)
        self.assertContains(guide_resp, 'Set Up a Django Web Application')

        # 2. Wi-Fi troubleshooting query
        wifi_resp = self._post_chat('wifi not working')
        self.assertEqual(wifi_resp.status_code, 200)
        wifi_links = wifi_resp.json()['bot_message']['links']
        self.assertTrue(any('wifi-network-troubleshooting' in lnk['url'] for lnk in wifi_links))

        # 3. Typo tolerance
        typo_resp = self._post_chat('pyhton install path')
        self.assertEqual(typo_resp.status_code, 200)
        typo_links = typo_resp.json()['bot_message']['links']
        self.assertTrue(any('python-installation-setup' in lnk['url'] for lnk in typo_links))

        # 4. Edit profile query
        profile_resp = self._post_chat('edit my profile')
        self.assertEqual(profile_resp.status_code, 200)
        profile_links = profile_resp.json()['bot_message']['links']
        self.assertTrue(any(lnk['url'] == reverse('assistant:edit_profile') for lnk in profile_links))

        # 5. Greeting query
        greet_resp = self._post_chat('hello')
        self.assertEqual(greet_resp.status_code, 200)
        self.assertIn('Technical Support Chatbot Assistant', greet_resp.json()['bot_message']['message'])

        # 6. Unrecognized query fallback
        unknown_resp = self._post_chat('quantum flux hyperdrive calibration')
        self.assertEqual(unknown_resp.status_code, 200)
        unknown_links = unknown_resp.json()['bot_message']['links']
        self.assertTrue(any(lnk['url'] == reverse('assistant:guide_list') for lnk in unknown_links))

    def test_chatbot_api_validation_persistence_and_clear(self):
        self.client.login(username='alice', password=self.user_password)

        empty_resp = self._post_chat('   ')
        self.assertEqual(empty_resp.status_code, 400)

        ok_resp = self._post_chat('xampp mysql port 3306 error')
        self.assertEqual(ok_resp.status_code, 200)
        self.assertEqual(ChatMessage.objects.filter(user=self.user).count(), 2)

        clear_resp = self.client.post(reverse('assistant:clear_chat_api'))
        self.assertEqual(clear_resp.status_code, 200)
        self.assertEqual(ChatMessage.objects.filter(user=self.user).count(), 0)

    def test_guide_list_search_and_category_filter(self):
        self.client.login(username='alice', password=self.user_password)

        resp = self.client.get(reverse('assistant:guide_list'), {'q': 'xampp'})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'XAMPP / MySQL')

        cat_resp = self.client.get(reverse('assistant:guide_list'), {'category': TechGuide.CATEGORY_HARDWARE})
        self.assertEqual(cat_resp.status_code, 200)
        self.assertContains(cat_resp, 'Bluetooth')
