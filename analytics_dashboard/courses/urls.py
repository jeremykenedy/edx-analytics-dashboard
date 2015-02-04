# pylint: disable=no-value-for-parameter

from django.conf.urls import url, patterns, include

from courses import views
from courses.views import enrollment, engagement, performance, csv

CONTENT_ID_PATTERN = r'(?P<content_id>[\.a-zA-Z0-9_+\/:-]+)'
COURSE_ID_PATTERN = r'(?P<course_id>[^/+]+[/+][^/+]+[/+][^/]+)'
PROBLEM_PART_ID_PATTERN = r'(?P<problem_part_id>[^/]+)'
ASSIGNMENT_ID_PATTERN = CONTENT_ID_PATTERN.replace('content_id', 'assignment_id')
PROBLEM_ID_PATTERN = CONTENT_ID_PATTERN.replace('content_id', 'problem_id')

# pylint: disable=line-too-long
answer_distribution_regex = r'^graded_content/assignments/{assignment_id}/problems/{problem_id}/parts/{part_id}/answer_distribution/$'.format(
    assignment_id=ASSIGNMENT_ID_PATTERN, problem_id=PROBLEM_ID_PATTERN, part_id=PROBLEM_PART_ID_PATTERN)

ENROLLMENT_URLS = patterns(
    '',
    url(r'^activity/$', enrollment.EnrollmentActivityView.as_view(), name='activity'),
    url(r'^geography/$', enrollment.EnrollmentGeographyView.as_view(), name='geography'),
    url(r'^demographics/age/$', enrollment.EnrollmentDemographicsAgeView.as_view(), name='demographics_age'),
    url(r'^demographics/education/$', enrollment.EnrollmentDemographicsEducationView.as_view(),
        name='demographics_education'),
    url(r'^demographics/gender/$', enrollment.EnrollmentDemographicsGenderView.as_view(), name='demographics_gender'),
)

ENGAGEMENT_URLS = patterns(
    '',
    url(r'^content/$', engagement.EngagementContentView.as_view(), name='content'),
)

PERFORMANCE_URLS = patterns(
    '',
    url(r'^graded_content/$', performance.PerformanceGradedContent.as_view(), name='graded_content'),
    url(r'^graded_content/(?P<assignment_type>[\w ]+)/$',
        performance.PerformanceGradedContentByType.as_view(),
        name='graded_content_by_type'),
    url(answer_distribution_regex, performance.PerformanceAnswerDistributionView.as_view(), name='answer_distribution'),

    # This MUST come AFTER the answer distribution pattern; otherwise, the answer distribution pattern
    # will be interpreted as an assignment pattern.
    url(r'^graded_content/assignments/{}/$'.format(ASSIGNMENT_ID_PATTERN),
        performance.PerformanceAssignment.as_view(),
        name='assignment'),
)

CSV_URLS = patterns(
    '',
    url(r'^enrollment/$', csv.CourseEnrollmentCSV.as_view(), name='enrollment'),
    url(r'^enrollment/geography/$', csv.CourseEnrollmentByCountryCSV.as_view(), name='enrollment_geography'),
    url(r'^enrollment/demographics/age/$',
        csv.CourseEnrollmentDemographicsAgeCSV.as_view(),
        name='enrollment_demographics_age'),
    url(r'^enrollment/demographics/education/$',
        csv.CourseEnrollmentDemographicsEducationCSV.as_view(),
        name='enrollment_demographics_education'),
    url(r'^enrollment/demographics/gender/$',
        csv.CourseEnrollmentDemographicsGenderCSV.as_view(),
        name='enrollment_demographics_gender'),
    url(r'^engagement/activity_trend/$',
        csv.CourseEngagementActivityTrendCSV.as_view(),
        name='engagement_activity_trend'),
    url(r'^performance/graded_content/problems/{}/answer_distribution/{}/$'.format(CONTENT_ID_PATTERN,
                                                                                   PROBLEM_PART_ID_PATTERN),
        csv.PerformanceAnswerDistributionCSV.as_view(),
        name='performance_answer_distribution'),
)

COURSE_URLS = patterns(
    '',
    # Course homepage. This should be the entry point for other applications linking to the course.
    url(r'^$', views.CourseHome.as_view(), name='home'),
    url(r'^enrollment/', include(ENROLLMENT_URLS, namespace='enrollment')),
    url(r'^engagement/', include(ENGAGEMENT_URLS, namespace='engagement')),
    url(r'^performance/', include(PERFORMANCE_URLS, namespace='performance')),
    url(r'^csv/', include(CSV_URLS, namespace='csv')),
)

urlpatterns = patterns(
    '',
    url('^$', views.CourseIndex.as_view(), name='index'),
    url(r'^{}/'.format(COURSE_ID_PATTERN), include(COURSE_URLS))
)
