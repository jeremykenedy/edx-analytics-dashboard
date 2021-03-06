import StringIO
import copy
import csv
import datetime

from analyticsclient.client import Client
from analyticsclient.constants import UNKNOWN_COUNTRY_CODE
import analyticsclient.constants.activity_type as AT
import analyticsclient.constants.education_level as EDUCATION_LEVEL
import analyticsclient.constants.gender as GENDER
from analyticsclient.constants import enrollment_modes

from courses.permissions import set_user_course_permissions
from courses.presenters.performance import AnswerDistributionEntry


CREATED_DATETIME = datetime.datetime(year=2014, month=2, day=2)
CREATED_DATETIME_STRING = CREATED_DATETIME.strftime(Client.DATETIME_FORMAT)
GAP_START = 2
GAP_END = 4


def get_mock_api_enrollment_data(course_id, include_verified=True):
    data = []
    start_date = datetime.date(year=2014, month=1, day=1)
    modes = enrollment_modes.ALL if include_verified else [enrollment_modes.AUDIT, enrollment_modes.HONOR]

    for index in range(31):
        date = start_date + datetime.timedelta(days=index)

        datum = {
            'date': date.strftime(Client.DATE_FORMAT),
            'course_id': unicode(course_id),
            'count': index * len(modes),
            'created': CREATED_DATETIME_STRING
        }

        for mode in modes:
            datum[mode] = index

        data.append(datum)

    return data


def get_mock_api_enrollment_data_with_gaps(course_id):
    data = get_mock_api_enrollment_data(course_id)
    data[GAP_START:GAP_END] = []
    return data


def get_mock_enrollment_summary(include_verified=True):
    summary = {
        'last_updated': CREATED_DATETIME,
        'current_enrollment': 60,
        'enrollment_change_last_7_days': 14,
    }

    if include_verified:
        summary.update({
            'current_enrollment': 120,
            'enrollment_change_last_7_days': 28,
            'verified_enrollment': 30,
            'verified_change_last_7_days': 7,
        })

    return summary


def get_mock_enrollment_summary_and_trend(course_id):
    return get_mock_enrollment_summary(), get_mock_presenter_enrollment_trend(course_id)


def _get_empty_enrollment(date):
    enrollment = {'count': 0, 'date': date}

    for mode in enrollment_modes.ALL:
        enrollment[mode] = 0

    return enrollment


def _clean_modes(data):
    for datum in data:
        datum[enrollment_modes.HONOR] = datum[enrollment_modes.AUDIT] + datum[enrollment_modes.HONOR]
        datum.pop(enrollment_modes.AUDIT)

    return data


def get_mock_presenter_enrollment_trend(course_id, include_verified=True):
    trend = get_mock_api_enrollment_data(course_id, include_verified=include_verified)
    trend = _clean_modes(trend)
    return trend


def parse_date(s):
    return datetime.datetime.strptime(s, Client.DATE_FORMAT).date()


def get_mock_presenter_enrollment_trend_with_gaps_filled(course_id):
    data = get_mock_presenter_enrollment_trend(course_id)
    data[GAP_START:GAP_END] = []

    datum = data[GAP_START - 1]

    for i in range(GAP_START, GAP_END):
        days = 1 + (i - GAP_START)
        item = copy.copy(datum)
        item['date'] = (parse_date(datum['date']) + datetime.timedelta(days=days)).strftime(Client.DATE_FORMAT)
        data.insert(i, item)

    return data


def get_mock_presenter_enrollment_data_small(course_id):
    data = [_get_empty_enrollment('2014-01-30'), get_mock_api_enrollment_data(course_id)[-1]]
    data = _clean_modes(data)

    return data


def get_mock_presenter_enrollment_summary_small():
    return {
        'last_updated': CREATED_DATETIME,
        'current_enrollment': 120,
        'enrollment_change_last_7_days': None,
        'verified_enrollment': 30,
        'verified_change_last_7_days': None,
    }


def get_mock_api_enrollment_geography_data(course_id):
    data = []
    items = ((u'USA', u'United States', 500), (None, UNKNOWN_COUNTRY_CODE, 300),
             (u'GER', u'Germany', 100), (u'CAN', u'Canada', 100))
    for item in items:
        data.append({'date': '2014-01-01', 'course_id': unicode(course_id), 'count': item[2],
                     'country': {'alpha3': item[0], 'name': item[1]}, 'created': CREATED_DATETIME_STRING})

    return data


def get_mock_api_enrollment_geography_data_limited(course_id):
    data = get_mock_api_enrollment_geography_data(course_id)
    return data[0:1]


def get_mock_presenter_enrollment_geography_data():
    data = [
        {'countryCode': 'USA', 'countryName': 'United States', 'count': 500, 'percent': 0.5},
        {'countryCode': 'GER', 'countryName': 'Germany', 'count': 100, 'percent': 0.1},
        {'countryCode': 'CAN', 'countryName': 'Canada', 'count': 100, 'percent': 0.1},
        {'countryCode': None, 'countryName': 'Unknown Country', 'count': 300, 'percent': 0.3},
    ]
    summary = {
        'last_updated': CREATED_DATETIME,
        'num_countries': 3,
        'top_countries': data[:3]  # The unknown entry is excluded from the list of top countries.
    }

    # Sort so that the unknown entry is in the correct location within the list.
    data = sorted(data, key=lambda i: i['count'], reverse=True)

    return summary, data


def get_mock_presenter_enrollment_geography_data_limited():
    """ Returns a smaller set of countries. """

    summary, data = get_mock_presenter_enrollment_geography_data()
    data = data[0:1]
    data[0]['percent'] = 1.0
    summary.update({
        'num_countries': 1,
        'top_countries': data
    })
    return summary, data


def get_mock_api_enrollment_gender_data(course_id):
    # top three are used in the summary (unknown is excluded)
    data = [
        {
            'course_id': course_id,
            'other': 123,
            GENDER.FEMALE: 456,
            GENDER.MALE: 789,
            GENDER.UNKNOWN: 1000,
            'date': '2014-09-21',
            'created': CREATED_DATETIME_STRING
        },
        {
            'course_id': course_id,
            'other': 500,
            GENDER.FEMALE: 100,
            GENDER.MALE: 400,
            GENDER.UNKNOWN: 1000,
            'date': '2014-09-22',
            'created': CREATED_DATETIME_STRING
        }
    ]

    return data


def get_presenter_enrollment_gender_data():
    return [
        {'gender': 'Female', 'percent': 0.1, 'order': 0},
        {'gender': 'Male', 'percent': 0.4, 'order': 1},
        {'gender': 'Other', 'percent': 0.5, 'order': 2}
    ]


def get_presenter_enrollment_gender_trend(course_id):
    return [
        {'course_id': course_id, GENDER.OTHER: 123, GENDER.FEMALE: 456, GENDER.MALE: 789, GENDER.UNKNOWN: 1000,
         'date': '2014-09-21', 'total': 2368,
         'created': CREATED_DATETIME_STRING},
        {'course_id': course_id, GENDER.OTHER: 500, GENDER.FEMALE: 100, GENDER.MALE: 400, GENDER.UNKNOWN: 1000,
         'date': '2014-09-22', 'total': 2000,
         'created': CREATED_DATETIME_STRING}
    ]


def get_presenter_gender(course_id):
    return CREATED_DATETIME, get_presenter_enrollment_gender_data(), get_presenter_enrollment_gender_trend(
        course_id), 0.5


def get_mock_api_enrollment_age_data(course_id):
    data = [
        {'course_id': course_id, 'birth_year': 1900, 'count': 100, 'created': CREATED_DATETIME_STRING},
        {'course_id': course_id, 'birth_year': 2000, 'count': 400, 'created': CREATED_DATETIME_STRING},
        {'course_id': course_id, 'birth_year': 2014, 'count': 500, 'created': CREATED_DATETIME_STRING},
        {'course_id': course_id, 'birth_year': None, 'count': 1000, 'created': CREATED_DATETIME_STRING}
    ]

    return data


def get_presenter_enrollment_binned_ages():
    current_year = datetime.date.today().year
    oldest = current_year - 100
    binned = []

    for year in range(oldest, current_year + 1):
        binned.append({'age': current_year - year, 'count': 0, 'percent': 0})

    # adjust 100+
    binned[0]['count'] = 100
    binned[0]['percent'] = 0.05

    # adjust year 2014
    index_2014 = 2014 - current_year - 1
    binned[index_2014]['count'] = 500
    binned[index_2014]['percent'] = 0.25

    # adjust year 2000
    index_2000 = 2000 - current_year - 1
    binned[index_2000]['count'] = 400
    binned[index_2000]['percent'] = 0.2

    binned.insert(0, {'age': 'Unknown', 'count': 1000, 'percent': 0.5})

    return binned[::-1]


def get_presenter_enrollment_ages_summary():
    current_year = datetime.date.today().year
    return {
        'median': (current_year * 2 - 2000 - 2014) * 0.5,
        'under_25': 0.9,
        'between_26_40': 0.0,
        'over_40': 0.1
    }


def get_presenter_ages():
    return CREATED_DATETIME, get_presenter_enrollment_ages_summary(), get_presenter_enrollment_binned_ages(), 0.5


def get_mock_api_enrollment_education_data(course_id):
    data = [
        {
            'course_id': course_id,
            'date': '2014-09-22',
            'education_level': EDUCATION_LEVEL.NONE,
            'count': 100,
            'created': CREATED_DATETIME_STRING
        },
        {
            'course_id': course_id,
            'date': '2014-09-22',
            'education_level': EDUCATION_LEVEL.OTHER,
            'count': 200,
            'created': CREATED_DATETIME_STRING
        },
        {
            'course_id': course_id,
            'date': '2014-09-22',
            'education_level': EDUCATION_LEVEL.PRIMARY,
            'count': 100,
            'created': CREATED_DATETIME_STRING
        },
        {
            'course_id': course_id,
            'date': '2014-09-22',
            'education_level': EDUCATION_LEVEL.JUNIOR_SECONDARY,
            'count': 100,
            'created': CREATED_DATETIME_STRING
        },
        {
            'course_id': course_id,
            'date': '2014-09-22',
            'education_level': EDUCATION_LEVEL.SECONDARY,
            'count': 100,
            'created': CREATED_DATETIME_STRING
        },
        {
            'course_id': course_id,
            'date': '2014-09-22',
            'education_level': EDUCATION_LEVEL.ASSOCIATES,
            'count': 100,
            'created': CREATED_DATETIME_STRING
        },
        {
            'course_id': course_id,
            'date': '2014-09-22',
            'education_level': EDUCATION_LEVEL.BACHELORS,
            'count': 100,
            'created': CREATED_DATETIME_STRING
        },
        {
            'course_id': course_id,
            'date': '2014-09-22',
            'education_level': EDUCATION_LEVEL.MASTERS,
            'count': 100,
            'created': CREATED_DATETIME_STRING
        },
        {
            'course_id': course_id,
            'date': '2014-09-22',
            'education_level': EDUCATION_LEVEL.DOCTORATE,
            'count': 100,
            'created': CREATED_DATETIME_STRING
        },
        {
            'course_id': course_id,
            'date': '2014-09-22',
            'education_level': None,
            'count': 1000,
            'created': CREATED_DATETIME_STRING
        },
    ]

    return data


def get_mock_presenter_enrollment_education_data():
    data = [
        {
            'educationLevel': 'None',
            'count': 100,
            'percent': 0.1,
            'order': 0
        },
        {
            'educationLevel': 'Primary',
            'count': 100,
            'percent': 0.1,
            'order': 1
        },
        {
            'educationLevel': 'Middle',
            'count': 100,
            'percent': 0.1,
            'order': 2
        },
        {
            'educationLevel': 'Secondary',
            'count': 100,
            'percent': 0.1,
            'order': 3
        },
        {
            'educationLevel': "Associate",
            'count': 100,
            'percent': 0.1,
            'order': 4
        },
        {
            'educationLevel': "Bachelor's",
            'count': 100,
            'percent': 0.1,
            'order': 5
        },
        {
            'educationLevel': "Master's",
            'count': 100,
            'percent': 0.1,
            'order': 6
        },
        {
            'educationLevel': 'Doctorate',
            'count': 100,
            'percent': 0.1,
            'order': 7
        },
        {
            'educationLevel': 'Other',
            'count': 200,
            'percent': 0.2,
            'order': 8
        },
        {
            'educationLevel': 'Unknown',
            'count': 1000
        }
    ]

    return data


def get_mock_presenter_enrollment_education_summary():
    return {
        'high_school_or_less': 0.3,
        'college': 0.2,
        'advanced': 0.2,
    }


def get_presenter_education():
    return (
        CREATED_DATETIME,
        get_mock_presenter_enrollment_education_summary(),
        get_mock_presenter_enrollment_education_data(),
        0.5
    )


def convert_list_of_dicts_to_csv(data, fieldnames=None):
    output = StringIO.StringIO()
    fieldnames = fieldnames or sorted(data[0].keys())

    writer = csv.DictWriter(output, fieldnames)
    writer.writeheader()
    writer.writerows(data)

    return output.getvalue()


def set_empty_permissions(user):
    set_user_course_permissions(user, [])
    return []


def mock_engagement_activity_summary_and_trend_data():
    trend = [
        {
            'weekEnding': '2013-01-08',
            AT.ANY: 100,
            AT.ATTEMPTED_PROBLEM: 301,
            AT.PLAYED_VIDEO: 1000,
            AT.POSTED_FORUM: 0,
        },
        {
            'weekEnding': '2013-01-01',
            AT.ANY: 1000,
            AT.ATTEMPTED_PROBLEM: 0,
            AT.PLAYED_VIDEO: 10000,
            AT.POSTED_FORUM: 45,
        }
    ]

    summary = {
        'last_updated': CREATED_DATETIME,
        AT.ANY: 100,
        AT.ATTEMPTED_PROBLEM: 301,
        AT.PLAYED_VIDEO: 1000,
        AT.POSTED_FORUM: 0,
    }

    return summary, trend


def get_mock_api_course_activity(course_id):
    return [
        {
            'course_id': unicode(course_id),
            'interval_end': '2014-09-01T000000',
            AT.ANY: 1000,
            AT.ATTEMPTED_PROBLEM: None,
            AT.PLAYED_VIDEO: 10000,
            AT.POSTED_FORUM: 45,
            'created': CREATED_DATETIME_STRING
        },
        {
            'course_id': unicode(course_id),
            'interval_end': '2014-09-08T000000',
            AT.ANY: 100,
            AT.ATTEMPTED_PROBLEM: 301,
            AT.PLAYED_VIDEO: 1000,
            AT.POSTED_FORUM: None,
            'created': CREATED_DATETIME_STRING
        },
    ]


# pylint: disable=unused-argument
def mock_course_activity(start_date=None, end_date=None):
    return get_mock_api_course_activity(u'edX/DemoX/Demo_Course')


def get_mock_api_answer_distribution_multiple_questions_data(course_id):
    answers = []
    total_count = 100

    for text_response in ['Asia', 'Europe', 'Africa']:
        answers.append({
            'answer_value': text_response,
            'correct': False,
            'count': total_count,
            'course_id': course_id,
            'created': CREATED_DATETIME_STRING,
            'module_id': 'i4x://edX/DemoX.1/problem/05d289c5ad3d47d48a77622c4a81ec36',
            'part_id': 'i4x-edX-DemoX_1-problem-5e3c6d6934494d87b3a025676c7517c1_2_1',
            'value_id': 'choice_0',
            'variant': None,
            'problem_display_name': 'Example problem',
            'question_text': 'Is this a text problem?'
        })
        total_count = total_count - 1
    answers[0]['correct'] = True

    for numeric_value in range(20):
        answers.append({
            'answer_value': numeric_value,
            'correct': False,
            'count': total_count,
            'course_id': course_id,
            'created': CREATED_DATETIME_STRING,
            'module_id': 'i4x://edX/DemoX.1/problem/05d289c5ad3d47d48a77622c4a81ec36',
            'part_id': 'i4x-edX-DemoX_1-problem-5e3c6d6934494d87b3a025676c7517c1_3_1',
            'value_id': None,
            'variant': None,
            'problem_display_name': 'Example problem',
            'question_text': 'Is this a numeric problem?'
        })
        total_count = total_count - 1
    answers[-1]['correct'] = True

    for randomized in range(5):
        answers.append({
            'answer_value': 0,
            'correct': True,
            'count': total_count,
            'course_id': course_id,
            'created': CREATED_DATETIME_STRING,
            'module_id': 'i4x://edX/DemoX.1/problem/05d289c5ad3d47d48a77622c4a81ec36',
            'part_id': 'i4x-edX-DemoX_1-problem-5e3c6d6934494d87b3a025676c7517c1_4_1',
            'value_id': None,
            'variant': randomized,
            'problem_display_name': 'Example problem',
            'question_text': 'Is this a randomized problem?'
        })
        total_count = total_count - 1

    return answers


def get_mock_api_answer_distribution_single_question_data(course_id):
    # get answers for one problem part
    return get_mock_api_answer_distribution_multiple_questions_data(course_id)[:3]


def get_presenter_performance_answer_distribution_multiple_questions():
    return [
        {
            'part_id': 'i4x-edX-DemoX_1-problem-5e3c6d6934494d87b3a025676c7517c1_2_1',
            'question': u'Submissions for Part 1: Is this a text problem?',
            'short_description': u'Part 1: Is this a text problem?',
            'problem_name': 'Example problem'
        },
        {
            'part_id': 'i4x-edX-DemoX_1-problem-5e3c6d6934494d87b3a025676c7517c1_3_1',
            'question': u'Submissions for Part 2: Is this a numeric problem?',
            'short_description': u'Part 2: Is this a numeric problem?',
            'problem_name': 'Example problem'
        },
        {
            'part_id': 'i4x-edX-DemoX_1-problem-5e3c6d6934494d87b3a025676c7517c1_4_1',
            'question': u'Submissions for Part 3: Is this a randomized problem?',
            'short_description': u'Part 3: Is this a randomized problem?',
            'problem_name': 'Example problem'
        }
    ]


def get_presenter_performance_answer_distribution_single_question():
    return [
        {
            'part_id': 'i4x-edX-DemoX_1-problem-5e3c6d6934494d87b3a025676c7517c1_2_1',
            'question': u'Submissions: Is this a text problem?',
            'short_description': u'Is this a text problem?',
            'problem_name': 'Example problem'
        }
    ]


def get_filtered_answer_distribution(course_id, problem_part_id):
    data = get_mock_api_answer_distribution_multiple_questions_data(course_id)
    return [d for d in data if d['part_id'] == problem_part_id]


def get_presenter_answer_distribution(course_id, problem_part_id):
    questions = get_presenter_performance_answer_distribution_multiple_questions()
    active_question = [i for i in questions if i['part_id'] == problem_part_id][0]['question']
    answer_distributions = get_filtered_answer_distribution(course_id, problem_part_id)
    answer_distribution_limited = answer_distributions[:12]
    is_random = answer_distribution_limited[0]['variant'] is not None
    try:
        float(answer_distribution_limited[0]['answer_value'])
        answer_type = 'numeric'
    except ValueError:
        answer_type = 'text'
    problem_part_description = 'Submissions for Part 1: Is this a text problem?'

    return AnswerDistributionEntry(CREATED_DATETIME, questions, active_question, answer_distributions,
                                   answer_distribution_limited, is_random, answer_type, problem_part_description)


def mock_course_name(course_id):
    return 'Test ' + course_id
