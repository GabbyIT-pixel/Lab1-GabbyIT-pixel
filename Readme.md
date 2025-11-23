# Grade Generator

This Python program allows a student to enter assignments, calculate weighted grades, GPA, pass/fail status, and save assignments into a CSV file.

---

## Features

- Collects assignment details:
  - Assignment name
  - Category (`FA` for Formative, `SA` for Summative)
  - Grade (0–100)
  - Weight (positive number)
- Calculates:
  - Weighted totals per category
  - Overall total grade
  - GPA on a 5.0 scale
  - Pass/Fail status for each category and overall
- Identifies formative assignments that need resubmission (score < 50) and suggests which assignment(s) to resubmit.
- Exports all assignments to `grades.csv`.

---

## Requirements

- Python 3 installed
- No external libraries required (uses built-in csv and sys modules)

---

## Usage

1. Open terminal or command prompt.
2. Navigate to the directory containing `grade-generator.py`.
3. Run the program:

##bash
python grade-generator.py

4. Follow the prompts:

Enter assignment name

Choose category (FA or SA)

Enter grade (0–100)

Enter weight (positive number)

Add more assignments or type n to finish

5. After entering all assignments:

View summary of total grades, GPA, and pass/fail status

If any formative assignments failed (<50), the program suggests resubmissions

Assignments are saved to grades.csv

Example Table

| Assignment                     | Category | Grade (%) | Weight | Final weight                   |
| ------------------------------ | -------- | --------- | ------ | ------------------------------ |
| Group Coding Lab               | FA       | 100       | 30     | 30                             |
| Discussion Forum               | FA       | 45        | 15     | 6.75                           |
| General Quiz                   | FA       | 49        | 15     | 7.35                           |
| Pre-Summative                  | SA       | 55        | 10     | 5.5                            |
| Individual Lab                 | SA       | 90        | 30     | 27                             |
| **Formatives (60)**            |          |           |        | 44.1                           |
| **Summatives (40)**            |          |           |        | 32.5                           |
| **GPA**                        |          |           |        | 3.83                           |
| **Status**                     |          |           |        | PASSED                         |
| **Available for resubmission** |          |           |        | Discussion Forum, General Quiz |

This table show how the program calculates final weighted scores, GPA, and highlights assignments available for resubmission.

Notes

Students pass only if they score ≥50% in both FA and SA categories.

For multiple failed FAs with the same highest weight, the student chooses which to resubmit.

CSV file grades.csv stores all assignments entered in the session.
