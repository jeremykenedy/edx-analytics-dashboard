import datetime
import re
from unittest import skipUnless

from bok_choy.web_app_test import WebAppTest

from acceptance_tests import ENABLE_COURSE_API
import common
from mixins import CoursePageTestsMixin
from pages import CoursePerformanceGradedContentPage, CoursePerformanceAnswerDistributionPage, \
    CoursePerformanceGradedContentByTypePage, CoursePerformanceAssignmentPage


_multiprocess_can_split_ = True


class CoursePerformancePageTestsMixin(CoursePageTestsMixin):
    def test_page(self):
        super(CoursePerformancePageTestsMixin, self).test_page()
        self._test_chart()
        self._test_table()

    def _test_chart(self):
        chart_selector = '#chart-view'
        self.fulfill_loading_promise(chart_selector)
        self.assertElementHasContent(chart_selector)

    def _test_table(self):
        raise NotImplementedError

    def _filter_children(self, blocks, key, **kwargs):
        """
        Given the blocks locates the nested graded or ungraded problems.
        """
        block = blocks[key]

        block_type = kwargs.pop(u'block_type', None)
        if block_type in kwargs:
            kwargs[u'type'] = block_type

        kwargs.setdefault(u'graded', False)

        matched = True
        for name, value in kwargs.iteritems():
            matched &= (block.get(name, None) == value)
            if not matched:
                break

        if matched:
            return [block]

        children = []
        for child in block[u'children']:
            children += self._filter_children(blocks, child, **kwargs)

        return children

    def _get_assignments(self, assignment_type=None):
        structure = self.course_api_client(self.page.course_id).structure.get()
        assignments = common.course_structure_to_assignments(structure, graded=True, assignment_type=assignment_type)

        # Retrieve the submissions from the Analytics Data API and create a lookup table.
        problems = self.course.problems()
        problems = dict((problem['module_id'], problem) for problem in problems)

        # Sum the submission counts
        for assignment in assignments:
            total = 0
            correct = 0

            for problem in assignment['problems']:
                submission_entry = problems.get(problem['id'], None)
                if submission_entry:
                    total += submission_entry['total_submissions']
                    correct += submission_entry['correct_submissions']

                    problem['total_submissions'] = submission_entry['total_submissions']
                    problem['correct_submissions'] = submission_entry['correct_submissions']

            assignment['total_submissions'] = total
            assignment['correct_submissions'] = correct

        return assignments

    def _get_data_update_message(self):
        problems = self.course.problems()
        last_updated = datetime.datetime.min

        for problem in problems:
            last_updated = max(last_updated, datetime.datetime.strptime(problem['created'], self.api_datetime_format))

        return 'Answer distribution data was last updated %(update_date)s at %(update_time)s UTC.' % \
               self.format_last_updated_date_and_time(last_updated)


@skipUnless(ENABLE_COURSE_API, 'Course API must be enabled to test the graded content page.')
class CoursePerformanceGradedContentTests(CoursePerformancePageTestsMixin, WebAppTest):
    """
    Tests for the course graded content page.
    """

    def _test_data_update_message(self):
        # There is no data update message displayed on this page.
        pass

    def _get_grading_policy(self):
        """
        Retrieve the course's grading policy from the Course API.
        """
        policy = self.course_api_client(self.page.course_id).grading_policy.get()

        for item in policy:
            weight = item['weight']
            item['weight_as_percentage'] = u'{:.0f}%'.format(weight * 100)

        return policy

    def setUp(self):
        super(CoursePerformanceGradedContentTests, self).setUp()
        self.page = CoursePerformanceGradedContentPage(self.browser)
        self.grading_policy = self._get_grading_policy()

    def _test_chart(self):
        """
        Test the assignment types display and values.
        """
        elements = self.page.browser.find_elements_by_css_selector('.grading-policy .policy-item')

        for index, element in enumerate(elements):
            grading_policy = self.grading_policy[index]
            assignment_type = grading_policy['assignment_type']

            # Verify the URL to view the assignments is correct.
            actual = element.find_element_by_css_selector('a').get_attribute('href')
            expected = u'{}{}/'.format(self.page.page_url, assignment_type)
            self.assertEqual(actual, expected)

            # Verify the displayed weight
            actual = element.find_element_by_css_selector('.weight').text
            weight = grading_policy['weight']
            expected = grading_policy['weight_as_percentage']
            self.assertEqual(actual, expected)

            # Verify the weighted column sizes
            r = r'col-md-(\d+)'
            classes = element.get_attribute('class')
            actual = int(re.match(r, classes).group(1))
            expected = int(weight * 12)
            self.assertEqual(actual, expected)

            # Verify the printed assignment type
            actual = element.find_element_by_css_selector('.type').text
            self.assertEqual(actual, assignment_type)

    def _test_table(self):
        table = self.page.browser.find_element_by_css_selector('.grading-configuration table')

        # Check the column headings
        cols = table.find_elements_by_css_selector('thead tr th')
        expected = [u'Assignment Type', u'Grade Percentage', u'Number of Assignments', u'Dropped Scores']
        self.assertRowTextEquals(cols, expected)

        # Check the actual data
        rows = table.find_elements_by_css_selector('tbody tr')
        self.assertEqual(len(rows), len(self.grading_policy))

        for index, row in enumerate(rows):
            grading_policy = self.grading_policy[index]
            cols = row.find_elements_by_css_selector('td')
            expected = [
                grading_policy['assignment_type'],
                grading_policy['weight_as_percentage'],
                unicode(grading_policy['count']),
                unicode(grading_policy['dropped'])
            ]
            self.assertRowTextEquals(cols, expected)


@skipUnless(ENABLE_COURSE_API, 'Course API must be enabled to test the course assignment type detail page.')
class CoursePerformanceGradedContentByTypeTests(CoursePerformancePageTestsMixin, WebAppTest):
    """
    Tests for the course assignment type detail page.
    """

    def setUp(self):
        super(CoursePerformanceGradedContentByTypeTests, self).setUp()
        self.page = CoursePerformanceGradedContentByTypePage(self.browser)
        self.assignment_type = self.page.assignment_type
        self.course = self.analytics_api_client.courses(self.page.course_id)
        self.assignments = self._get_assignments(self.assignment_type)

    def _test_table(self):
        table = self.page.browser.find_element_by_css_selector('.section-data-table table')

        # Check the column headings
        cols = table.find_elements_by_css_selector('thead tr th')
        expected = [u'Order', u'Assignment Name', u'Problems', u'Total Submissions', u'Correct Submissions',
                    u'Incorrect Submissions']
        self.assertRowTextEquals(cols, expected)

        # Check the row texts
        rows = table.find_elements_by_css_selector('tbody tr')
        self.assertEqual(len(rows), len(self.assignments))

        for index, row in enumerate(rows):
            assignment = self.assignments[index]
            cols = row.find_elements_by_css_selector('td')
            expected = [
                unicode(index + 1),
                assignment['name'],
                unicode(len(assignment['problems'])),
                self.format_number(assignment['total_submissions']),
                self.format_number(assignment['correct_submissions']),
                self.format_number(assignment['total_submissions'] - assignment['correct_submissions']),
            ]
            self.assertRowTextEquals(cols, expected)


@skipUnless(ENABLE_COURSE_API, 'Course API must be enabled to test the course assignment detail page.')
class CoursePerformanceAssignmentTests(CoursePerformancePageTestsMixin, WebAppTest):
    """
    Tests for the course assignment detail page.
    """

    def _get_assignment(self):
        assignments = self._get_assignments()
        for assignment in assignments:
            if assignment[u'id'] == self.assignment_id:
                return assignment

        raise AttributeError('Assignment not found!')

    def setUp(self):
        super(CoursePerformanceAssignmentTests, self).setUp()
        self.page = CoursePerformanceAssignmentPage(self.browser)
        self.assignment_id = self.page.assignment_id
        self.course = self.analytics_api_client.courses(self.page.course_id)
        self.assignment = self._get_assignment()

    def _test_table(self):
        table = self.page.browser.find_element_by_css_selector('.section-data-table table')

        # Check the column headings
        cols = table.find_elements_by_css_selector('thead tr th')
        expected = [u'Order', u'Problem Name', u'Total Submissions', u'Correct Submissions', u'Incorrect Submissions']
        self.assertRowTextEquals(cols, expected)

        # Check the row texts
        rows = table.find_elements_by_css_selector('tbody tr')
        problems = self.assignment['problems']
        self.assertEqual(len(rows), len(problems))

        for index, row in enumerate(rows):
            problem = problems[index]
            cols = row.find_elements_by_css_selector('td')

            expected = [
                unicode(index + 1),
                problem['name'],
                self.format_number(problem['total_submissions']),
                self.format_number(problem['correct_submissions']),
                self.format_number(problem['total_submissions'] - problem['correct_submissions']),
            ]
            self.assertRowTextEquals(cols, expected)


@skipUnless(ENABLE_COURSE_API, 'Course API must be enabled to test the answer distribution page.')
class CoursePerformanceAnswerDistributionTests(CoursePerformancePageTestsMixin, WebAppTest):
    """
    Tests for the course problem answer distribution page.
    """

    help_path = 'performance/index.html'

    def setUp(self):
        super(CoursePerformanceAnswerDistributionTests, self).setUp()
        self.page = CoursePerformanceAnswerDistributionPage(self.browser)
        self.course = self.analytics_api_client.courses(self.page.course_id)
        self.module = self.analytics_api_client.modules(self.page.course_id, self.page.problem_id)
        api_response = self.module.answer_distribution()
        data = [i for i in api_response if i['part_id'] == self.page.part_id]
        self.answer_distribution = sorted(data, key=lambda a: a['count'], reverse=True)

    def test_page(self):
        super(CoursePerformanceAnswerDistributionTests, self).test_page()
        self._test_heading_question()
        self._test_problem_description()

    def _test_heading_question(self):
        element = self.page.q(css='.section-heading')
        self.assertEqual(element.text[0], u'How did students answer this problem?')

    def _test_problem_description(self):
        section_selector = '.problem-description'

        element = self.page.q(css=section_selector + ' p')
        self.assertIsNotNone(element[0])

        self.assertValidHref(section_selector + ' a')

    def _test_chart(self):
        chart_selector = '#performance-chart-view'
        self.fulfill_loading_promise(chart_selector)
        self.assertElementHasContent(chart_selector)

        element = self.page.q(css='#distQuestionsMenu')
        self.assertIn('Submissions for Part', element[0].text)

        container_selector = '.analytics-chart-container'
        element = self.page.q(css=container_selector + ' i')
        expected_tooltip = 'This graph shows answers submitted by at least one student, ' \
                           'and the number of students who submitted each answer. The most frequently submitted answers, ' \
                           'up to 12, are included.'
        self.assertEqual(element[0].get_attribute('data-original-title'), expected_tooltip)

    def _test_table(self):
        table_section_selector = "div[data-role=performance-table]"
        self.assertTable(table_section_selector, ['Answer', 'Correct', 'Submission Count'],
                         'a[data-role=performance-csv]')

        rows = self.page.browser.find_elements_by_css_selector('{} tbody tr'.format(table_section_selector))

        value_field = 'answer_value'

        for i, row in enumerate(rows):
            answer = self.answer_distribution[i]
            columns = row.find_elements_by_css_selector('td')

            actual = []
            for col in columns:
                actual.append(col.text)

            expected = [answer[value_field]]
            correct = '-'
            if answer['correct']:
                correct = u'Correct'
            expected.append(correct)
            expected.append(self.format_number(answer['count']))

            self.assertListEqual(actual, expected)
            self.assertIn('text-right', columns[2].get_attribute('class'))
