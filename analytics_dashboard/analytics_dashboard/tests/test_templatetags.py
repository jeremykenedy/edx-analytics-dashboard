#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.template import Template, Context, TemplateSyntaxError
from django.test import TestCase
from opaque_keys.edx.keys import CourseKey
from analytics_dashboard.templatetags.dashboard_extras import format_course_key

from analytics_dashboard.templatetags import dashboard_extras


class DashboardExtraTests(TestCase):
    def test_settings_value(self):
        template = Template(
            "{% load dashboard_extras %}"
            "{% settings_value \"FAKE_SETTING\" %}"
        )

        # If setting is not found, tag returns None.
        self.assertRaises(AttributeError, template.render, Context())

        with self.settings(FAKE_SETTING='edX'):
            # If setting is found, tag simply displays setting value.
            self.assertEqual(template.render(Context()), "edX")

    def assertTextCaptured(self, expected):
        template = Template(
            "{% load dashboard_extras %}"
            "{% captureas foo %}{{ expected }}{%endcaptureas%}"
            "{{ foo }}"
        )
        # Tag should render the value captured in the block.
        self.assertEqual(template.render(Context({'expected': expected})), expected)

    def test_captureas(self):
        # Tag requires a variable name.
        self.assertRaises(TemplateSyntaxError, Template,
                          "{% load dashboard_extras %}" "{% captureas %}42{%endcaptureas%}")

        self.assertTextCaptured('42')

    def test_captureas_unicode(self):
        self.assertTextCaptured(u'★❤')

    def test_format_course_key(self):
        values = [('edX/DemoX/Demo_Course', 'edX/DemoX/Demo_Course'),
                  ('course-v1:edX+DemoX+Demo_2014', 'edX/DemoX/Demo_2014')]
        for course_id, expected in values:
            # Test with CourseKey
            course_key = CourseKey.from_string(course_id)
            self.assertEqual(format_course_key(course_key), expected)

            # Test with string
            self.assertEqual(format_course_key(course_id), expected)

    def test_metric_percentage(self):
        self.assertEqual(dashboard_extras.metric_percentage(0), '0%')
        self.assertEqual(dashboard_extras.metric_percentage(0.009), '< 1%')
        self.assertEqual(dashboard_extras.metric_percentage(0.5066), '50.7%')
        self.assertEqual(dashboard_extras.metric_percentage(0.5044), '50.4%')
