.. _Performance_Answers:

#############################
Graded Content Submissions
#############################

How are students answering questions? Graded content submissions show you the
responses that students submit for graded problems and help you evaluate what
they find difficult.

Student submissions are updated every day. The computations include responses
to problems through the end of the previous day (23:59 UTC).

*************************************
Gaining Insight into Course Problems
*************************************

Student submission data is available in edX Insights for problem components of
these types:

* Checkboxes

* Dropdown

* Multiple choice

* Numerical input

* Text input

* Math expression input

EdX Insights delivers submission data in a bar chart and a report that you can
view or download. For problem components that include more than one question
or part, edX Insights presents a separate chart and report for each part. You
select each part from the drop-down list in the top corner of the chart.
Descriptions of the chart and report follow. For detailed information about
the computations, see :ref:`Reference`.

======================================
Submissions Chart
======================================

The bars on this chart represent the number of enrolled students who submitted
a particular answer to a question in a problem component. The x-axis includes
the most frequently submitted answers, up to a maximum of 12. Due to space
limitations, the question text that is used to label the x-axis might be
truncated. Moving your cursor over each bar shows a longer version of the
answer.

To review the problem component in the LMS as a student does, click **View
Live** and then at the top of the page click **Staff View**. The LMS displays
the corresponding page in Student View. For more information, see `View Your
Live Course`_.

All submitted answers, and complete answer values, are available for review in
tabular format at the bottom of the page and can also be downloaded.

.. Examples of the graded content submissions chart follow. In the first example,

An example of the graded content submissions chart follows. In this example,
most students selected the correct answer for a multiple choice problem.

.. image:: ../images/answer_dist_easy.png
   :alt: A bar chart showing that most students selected the correct answer
       out of four possible choices

.. TsinghuaX/00690242_1x/problem/268b43628e6d45f79c52453a590f9829/answerdistribution/i4x-TsinghuaX-00690242_1x-problem-268b43628e6d45f79c52453a590f9829_2_1/

.. TBD: The second example shows... 

.. second example - a more nuanced question? or one that might be misconstrued?

.. The last example is for a problem that has several parts. You use the list control above the chart to choose each of the parts. When you select a different part, both the chart and the report refresh with data for that problem part.

.. TBD: image to come

.. image of the first part of a multipart problem with the dropdown circled

.. note:: Problems that use the randomization setting in Studio result in 
 many possible submission variants, both correct and incorrect. As a result,
 edX Insights does not attempt to present a chart of responses to these
 problems. Download the student submissions report to analyze responses of
 interest.

For more information, see the :ref:`Reference`.

======================================
Submissions Report
======================================

A report with a row for each problem-answer combination submitted by your
students is available for review or download. The report columns show each
submitted answer, identify the correct answer or answers, and provide the
number of students who selected or provided that answer.

To download the Submissions report in a comma-separated value
file, click **Download CSV**.

The report and the file include one row for each problem-answer combination
submitted by a student. For example, consider a dropdown problem that has
five possible answers. The report or file contains up to five rows, one for
each answer selected by at least one student.

For problems that enable the randomization feature in Studio, there is one row
for each problem-variant-answer combination selected by at least one student.
For more information about problem randomization, see `Randomization`_.

See the :ref:`Reference` for a detailed description of each column.

*******************************************************
Analytics in Action: Interpreting Student Submissions
*******************************************************

A review of the distribution of student submissions for a problem can lead to
discoveries about your students and about your course.

* You can assess how difficult the problem is for students to answer correctly. 

* You can detect common mistakes.

* You can understand student misconceptions.

* You can find errors in problem components.

===============================================
Researching Unexpected Difficulties
===============================================

For problem types that provide both the question and a set of possible answers
(checkboxes, dropdown, and multiple choice), submission data helps you assess
how difficult it is for students to select the correct answer. With the
submissions chart, you can visually contrast the number of students who select
incorrect answers with the number who answer correctly.

If the number of students who answer the problem incorrectly surprises you,
research can reveal a variety of causes. Your investigation might begin with
some of these questions.

* Is the text of the question and of its possible answers clear? Has it been
  translated accurately?

* Does the course outline include relevant course content before the problem,
  or after it?

* Are all of the course prerequisites presented to potential students?

* Does the problem rely on student access to a video or textbook? Do students
  have access to alternatives: are there transcripts for the videos, and can
  the textbook files be read by a screen reader?

* Are students relying on conventional wisdom to answer the question instead
  of newly acquired knowledge?

The results of your investigation can guide changes to future course runs.

.. others?

===============================================
Investigating Similar Responses
===============================================

For open-ended problem types that provide only the question (numerical, text,
and math expression input), submission data can help you identify similar
responses. In the submissions report you have access to every answer submitted
by a student. The chart, however, presents only the 12 most frequently
submitted responses. Your initial investigation into how students answer a
question can begin with this manageably-sized set.

For example, you create a text input problem with a single correct answer,
"Warfarin". When you review its submissions chart, you notice how many
similar, but incorrect, variations your students provide, including "warfarin
sodium" and "Warfarin or Coumadin". 

The proximity of these variations in the chart might reassure you that more
students understand the relevant course material than is indicated by the
number who actually provided the correct answer. If so, it might also prompt
you to update the problem so that the additional variations of the answer are
evaluated as correct. Alternatively, you might decide to revise the question
so that your parameters for the correct response are clearer, or change the
problem type to a more appropriate one.



.. _Randomization: http://edx.readthedocs.org/projects/edx-partner-course-staff/en/latest/creating_content/create_problem.html#randomization

.. _View Your Live Course: http://edx.readthedocs.org/projects/edx-partner-course-staff/en/latest/developing_course/testing_courseware.html?highlight=view%20live#view-your-live-course
