import json
import unittest

import mock
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory, override_settings

from django_factory_boy import auth as auth_factories

from conference.tests.factories.attendee_profile import AttendeeProfileFactory

from django.conf import settings

from conference.tests.factories.conference import ConferenceFactory


class TestWhosComing(TestCase):
    def setUp(self):
        self.user = auth_factories.UserFactory(password='password1234', is_superuser=True)
        is_logged = self.client.login(username=self.user.username,
                                      password='password1234')
        AttendeeProfileFactory(user=self.user)
        self.assertTrue(is_logged)

    @override_settings(CONFERENCE_CONFERENCE='epbeta', DEBUG=False)
    def test_p3_whos_coming_no_conference(self):
        url = reverse('p3-whos-coming')
        conference = ConferenceFactory(code='epbeta')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('p3-whos-coming-conference', kwargs={
            'conference': conference.pk,
        }))


    def test_p3_whos_coming_with_conference(self):
        # p3-whos-coming-conference -> p3.views.whos_coming
        # FIXME: The conference parameter has a default value to None, but the url does not accept a empty value
        conference = ConferenceFactory(code='epbeta')
        url = reverse('p3-whos-coming-conference', kwargs={
            'conference': conference.pk
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # FIXME: Test the query string speaker, tags, country


class TestView(TestCase):
    def setUp(self):
        self.user = auth_factories.UserFactory(password='password1234', is_superuser=True)
        is_logged = self.client.login(username=self.user.username,
                                      password='password1234')
        AttendeeProfileFactory(user=self.user)
        self.assertTrue(is_logged)

    def test_p3_billing_with_no_user_cart(self):
        # p3-billing -> p3.views.cart.billing
        url = reverse('p3-billing')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('p3-cart'), fetch_redirect_response=False)

    def test_p3_billing_no_ticket(self):
        # p3-billing -> p3.views.cart.billing
        url = reverse('p3-billing')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('p3-cart'), fetch_redirect_response=False)

    @override_settings(DEBUG=False)
    def test_p3_calculator_get_default_values(self):
        # p3-calculator -> p3.views.cart.calculator
        url = reverse('p3-calculator')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('content-type'), 'application/json')
        self.assertJSONEqual(response.content, {'tickets': [], 'coupon': 0, 'total': 0})

    @unittest.skip("FIXME")
    def test_p3_hotel_report(self):
        # p3-hotel-report -> p3.views.reports.hotel_report
        url = reverse('p3-hotel-report')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @unittest.skip("FIXME")
    def test_p3_live(self):
        # p3-live -> p3.views.live.live
        url = reverse('p3-live')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    @unittest.skip("FIXME")
    def test_p3_live_track_events(self):
        # p3-live-track-events -> p3.views.live.live_track_events
        url = reverse('p3-live-track-events')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    @unittest.skip("FIXME")
    def test_p3_live_track_video(self):
        # p3-live-track-video -> p3.views.live.live_track_video
        url = reverse('p3-live-track-video')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    @unittest.skip("FIXME")
    def test_p3_live_events(self):
        # p3-live-events -> p3.views.live.live_events
        url = reverse('p3-live-events')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    @unittest.skip("FIXME")
    def test_p3_map_js(self):
        # p3-map-js -> p3.views.map_js
        url = reverse('p3-map-js')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    @unittest.skip("FIXME")
    def test_p3_my_schedule(self):
        # p3-my-schedule -> p3.views.schedule.jump_to_my_schedule
        url = reverse('p3-my-schedule')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        redirect_url = reverse('p3-schedule-my-schedule', kwargs={
            'conference': settings.CONFERENCE_CONFERENCE
        })
        self.assertRedirects(response, redirect_url, fetch_redirect_response=False )

    @unittest.skip("FIXME")
    def test_p3_account_data_get(self):
        # p3-account-data -> p3.views.profile.p3_account_data
        url = reverse('p3-account-data')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @unittest.skip("Fix the test with POST method for p3_account_data")
    def test_p3_account_data_post(self):
        # p3-account-data -> p3.views.profile.p3_account_data
        url = reverse('p3-account-data')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)


    @unittest.skip("FIXME")
    def test_p3_account_email(self):
        # p3-account-email -> p3.views.profile.p3_account_email
        url = reverse('p3-account-email')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    @unittest.skip("FIXME")
    def test_p3_account_spam_control(self):
        # p3-account-spam-control -> p3.views.profile.p3_account_spam_control
        url = reverse('p3-account-spam-control')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    @unittest.skip("FIXME")
    def test_p3_profile_json(self):
        # p3-profile-json -> p3.views.profile.p3_profile
        url = reverse('p3-profile-json')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    @unittest.skip("FIXME")
    def test_p3_profile(self):
        # p3-profile -> p3.views.profile.p3_profile
        url = reverse('p3-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    @unittest.skip("FIXME")
    def test_p3_profile_avatar(self):
        # p3-profile-avatar -> p3.views.profile.p3_profile_avatar
        url = reverse('p3-profile-avatar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    @unittest.skip("FIXME")
    def test_p3_profile_message(self):
        # p3-profile-message -> p3.views.profile.p3_profile_message
        url = reverse('p3-profile-message')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    @unittest.skip("FIXME")
    def test_p3_schedule_ics(self):
        # p3-schedule-ics -> p3.views.schedule.schedule_ics
        url = reverse('p3-schedule-ics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    @unittest.skip("FIXME")
    def test_p3_schedule(self):
        # p3-schedule -> p3.views.schedule.schedule
        url = reverse('p3-schedule')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    @unittest.skip("FIXME")
    def test_p3_schedule_list(self):
        # p3-schedule-list -> p3.views.schedule.schedule_list
        url = reverse('p3-schedule-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    @unittest.skip("FIXME")
    def test_p3_schedule_my_schedule_ics(self):
        # p3-schedule-my-schedule-ics -> p3.views.schedule.schedule_ics
        url = reverse('p3-schedule-my-schedule-ics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    @unittest.skip("FIXME")
    def test_p3_schedule_my_schedule(self):
        # p3-schedule-my-schedule -> p3.views.schedule.my_schedule
        url = reverse('p3-schedule-my-schedule')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    @unittest.skip("FIXME")
    def test_p3_sprint_submission(self):
        # p3-sprint-submission -> p3.views.sprint_submission
        url = reverse('p3-sprint-submission')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    @unittest.skip("FIXME")
    def test_p3_sprints(self):
        # p3-sprints -> p3.views.sprints
        url = reverse('p3-sprints')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    @unittest.skip("FIXME")
    def test_p3_sprint(self):
        # p3-sprint -> p3.views.sprint
        url = reverse('p3-sprint')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    @unittest.skip("FIXME")
    def test_p3_tickets(self):
        # p3-tickets -> p3.views.tickets
        url = reverse('p3-tickets')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    @unittest.skip("FIXME")
    def test_p3_ticket(self):
        # p3-ticket -> p3.views.ticket
        url = reverse('p3-ticket')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    @unittest.skip("FIXME")
    def test_p3_user(self):
        # p3-user -> p3.views.user
        url = reverse('p3-user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
