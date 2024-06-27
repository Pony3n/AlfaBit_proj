from django.test import TestCase
from ..models import Lead, LeadState


class LeadStateTransitionTests(TestCase):

    def setUp(self):
        self.state_new = LeadState.objects.create(name='New')
        self.state_in_progress = LeadState.objects.create(name='In Progress')
        self.state_postponed = LeadState.objects.create(name='Postponed')
        self.state_done = LeadState.objects.create(name='Done')

        self.lead = Lead.objects.create(name='Test Lead', state=self.state_new)

    def test_valid_transition_new_to_in_progress(self):
        self.lead.change_state(LeadState.STATE_IN_PROGRESS)
        self.assertEqual(self.lead.state.id, LeadState.STATE_IN_PROGRESS)

    def test_valid_transition_in_progress_to_postponed(self):
        self.lead.change_state(LeadState.STATE_IN_PROGRESS)
        self.lead.change_state(LeadState.STATE_POSTPONED)
        self.assertEqual(self.lead.state.id, LeadState.STATE_POSTPONED)

    def test_valid_transition_in_progress_to_done(self):
        self.lead.change_state(LeadState.STATE_IN_PROGRESS)
        self.lead.change_state(LeadState.STATE_DONE)
        self.assertEqual(self.lead.state.id, LeadState.STATE_DONE)

    def test_valid_transition_postponed_to_in_progress(self):
        self.lead.change_state(LeadState.STATE_IN_PROGRESS)
        self.lead.change_state(LeadState.STATE_POSTPONED)
        self.lead.change_state(LeadState.STATE_IN_PROGRESS)
        self.assertEqual(self.lead.state.id, LeadState.STATE_IN_PROGRESS)

    def test_valid_transition_postponed_to_done(self):
        self.lead.change_state(LeadState.STATE_IN_PROGRESS)
        self.lead.change_state(LeadState.STATE_POSTPONED)
        self.lead.change_state(LeadState.STATE_DONE)
        self.assertEqual(self.lead.state.id, LeadState.STATE_DONE)

    def test_invalid_transition(self):
        self.assertEqual(self.lead.state, self.state_new)

        with self.assertRaises(ValueError):
            self.lead.change_state(self.state_done.id)

        self.assertEqual(self.lead.state, self.state_new)

# python manage.py test app_handler.tests.test_models
# Из директории handler