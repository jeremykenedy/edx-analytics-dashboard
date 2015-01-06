.. _Performance_Answers:

#############################
Student Answers
#############################

.. revise title to match UI when available

You can use the Student Answer Distribution report to review student responses
to assignments, which can then help you evaluate the structure and completeness
of your courseware and problem components.

Charts can help make your students' common misconceptions  easier to
identify.

You can adjust your course content based on common student mistakes. While most
students in this example selected the correct answer, the number of incorrect
answer(s) can guide future changes to the courseware.


As an example, you define a text input question in Studio to have a single
correct answer, "Warfarin". When you produce the Student Answer Distribution
report, you verify that this answer was in fact marked correct. However, as you view the report you notice other student answers that you did
not set up to be marked as correct in Studio, but that you might (or might not)
also consider to be correct, such as "Warfarin or Coumadin". For
future iterations of your course you may want to revise the question or update
the problem to evaluate additional variations of the answer as correct.


For certain types of problems in your course, you can download a CSV file with
data about the distribution of student answers. Student answer distribution data
is included in the file for problems of these types:

* Checkboxes (``<choiceresponse>``)
* Dropdown (``<optionresponse>``)
* Multiple choice (``<multiplechoiceresponse>``)
* Numerical input (``<numericalresponse>``)
* Text input (``<stringresponse>``)
* Math expression input (``<formularesponse>``)

The file includes a row for each problem-answer combination selected by your
students. For example, for a problem that has a total of five possible answers
the file includes up to five rows, one for each answer selected by at least one
student. For problems with **Randomization** enabled in Studio (sometimes
called rerandomization), there is one row for each problem-variant-answer
combination selected by your students.