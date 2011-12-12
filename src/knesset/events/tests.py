"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

import datetime
from datetime import timedelta

import vobject

from django.test import TestCase
from django.core.urlresolvers import reverse

from models import Event

now = datetime.datetime.now()

class SimpleTest(TestCase):
    def setUp(self):
        self.ev1 = Event.objects.create(when=now, what="ev1")
        self.ev2 = Event.objects.create(when=now + timedelta(days=1), when_over=now + timedelta(days=1,hours=2), when_over_guessed=False, what="future=%s" % ''.join(str(x % 10) for x in xrange(300)))

    def testFutureEvent(self):
        """
        Tests Event.is_future property.
        """
        tomorrow = now+datetime.timedelta(1)
        ev2 = Event.objects.create(when=tomorrow, what="ev2")
        self.assertTrue(ev2.is_future)
        ev2.delete()

    def testIcalenderSummaryLength(self):
        """
        Tests that the icalendar view uses summary_length
        correctly.
        """
        summary_length = 123
        res = self.client.get(reverse('event-icalendar', kwargs={'summary_length':summary_length}))
        self.assertEqual(res.status_code,200)
        vcal = vobject.base.readOne(res.content)
        for vevent in vcal.components():
            if vevent.name != 'VEVENT':
                continue
            self.assertEqual(len(vevent.summary.value), summary_length)
