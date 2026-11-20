import math
import os


def _is_finite_number(value: object) -> bool:
    """Return True for finite int/float values, excluding booleans."""
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
    )


COURSES: dict[int, list[tuple[str, str, float]]] = {
    1: [
        ("MS-251", "Probability & Statistics", 3.0),
        ("GE-160", "Applications of ICT", 3.0),
        ("GE-169", "Applied Physics", 3.0),
        ("GE-167", "Discrete Structures", 3.0),
        ("HQ-001", "Quran Translation I", 0.5),
        ("GE-190", "Functional English", 3.0),
    ],
    2: [
        ("CC-112", "Programming Fundamentals", 3.0),
        ("CC-112-L", "Programming Fundamentals Lab", 1.0),
        ("CC-110", "Digital Logic Design", 2.0),
        ("CC-110-L", "Digital Logic Design Lab", 1.0),
        ("MS-252", "Linear Algebra", 3.0),
        ("GE-191", "Expository Writing", 3.0),
        ("GE-163", "Islamic Studies", 2.0),
        ("HQ-002", "Quran Translation II", 0.5),
    ],
    3: [
        ("CC-211", "Object Oriented Programming", 3.0),
        ("CC-211-L", "Object Oriented Programming Lab", 1.0),
        ("CC-215", "Database Systems", 3.0),
        ("CC-215-L", "Database Systems Lab", 1.0),
        ("CC-210", "Computer Organization & Assembly Language", 3.0),
        ("GE-162", "Calculus & Analytical Geometry", 3.0),
        ("GE-192", "Introduction to Management", 2.0),
        ("HQ-003", "Quran Translation III", 0.5),
    ],
    4: [
        ("CC-213", "Data Structures", 3.0),
        ("CC-213-L", "Data Structures Lab", 1.0),
        ("CC-312", "Information Security", 3.0),
        ("CC-214", "Computer Networks", 3.0),
        ("CC-212", "Software Engineering", 3.0),
        ("DC-220", "Advanced Database Management Systems", 3.0),
        ("HQ-004", "Quran Translation IV", 0.5),
    ],
    5: [
        ("CC-313", "Analysis of Algorithms", 3.0),
        ("CC-310", "Artificial Intelligence", 3.0),
        ("DC-320", "Theory of Automata and Formal Languages", 3.0),
        ("DC-321", "Human Computer Interaction", 3.0),
        ("DC-322", "Computer Architecture", 3.0),
        ("EC-330", "Web Technologies / Elective", 3.0),
        ("HQ-005", "Quran Translation V", 0.5),
    ],
    6: [
        ("CC-311", "Operating Systems", 3.0),
        ("EC-333", "Mobile Application Development / Elective", 3.0),
        ("EC-324", "Software Construction & Development / Elective", 3.0),
        ("EC-335", "Machine Learning / Elective", 3.0),
        ("EC-334", "Game Design and Development / Elective", 3.0),
        ("MS-253", "Multivariable Calculus", 3.0),
        ("HQ-006", "Quran Translation VI", 0.5),
    ],
    7: [
        ("CC-411", "Final Year Project I", 2.0),
        ("DC-328", "Parallel & Distributed Computing", 3.0),
        ("EC-345", "Computer Vision / Elective", 3.0),
        ("EC-425", "Software Quality Engineering / Elective", 3.0),
        ("MS-254", "Technical and Business Writing", 3.0),
        ("GE-263", "Entrepreneurship", 2.0),
        ("GE-262", "Professional Practices", 2.0),
        ("HQ-007", "Quran Translation VII", 0.5),
    ],
    8: [
        ("CC-412", "Final Year Project II", 4.0),
        ("DC-421", "Compiler Construction", 3.0),
        ("UE-272", "Introduction to Marketing", 3.0),
        ("GE-168", "Ideology and Constitution of Pakistan", 2.0),
        ("GE-363", "Civics and Community Engagement", 2.0),
        ("HQ-008", "Quran Translation VIII", 0.5),
    ],
}


def marks_to_grade_points(marks: int | float) -> float | str:
    """Convert marks (0-100) to grade points using the PUCIT grade bands."""
    if not _is_finite_number(marks):
        return "Error: marks must be a valid finite number"
    if not 0 <= marks <= 100:
        return "Error: marks must be between 0 and 100"

    if marks >= 85:
        return 4.0
    if marks >= 80:
        return 3.7
    if marks >= 75:
        return 3.3
    if marks >= 70:
        return 3.0
    if marks >= 65:
        return 2.7
    if marks >= 61:
        return 2.3
    if marks >= 58:
        return 2.0
    if marks >= 55:
        return 1.7
    if marks >= 50:
        return 1.0
    return 0.0


def calculate_semester_gpa(
    grade_points: list[float], credit_hours: list[float]
) -> float | str:
    """Calculate credit-weighted semester GPA from grade points and course credits."""
    if not grade_points or not credit_hours:
        return "Error: grade_points and credit_hours lists cannot be empty"
    if len(grade_points) != len(credit_hours):
        return "Error: grade_points and credit_hours lists must have the same length"

    for grade_point in grade_points:
        if not _is_finite_number(grade_point) or not 0.0 <= grade_point <= 4.0:
            return "Error: grade points must be finite numbers between 0.0 and 4.0"

    for credit in credit_hours:
        if not _is_finite_number(credit) or credit <= 0.0:
            return "Error: credit hours must be finite numbers greater than 0"

    total_credit_hours = sum(credit_hours)
    weighted_points = sum(
        grade_point * credit
        for grade_point, credit in zip(grade_points, credit_hours)
    )
    return round(weighted_points / total_credit_hours, 2)


def calculate_new_cgpa(
    current_cgpa: float,
    completed_credit_hours: float,
    semester_gpa: float,
    semester_credit_hours: float,
) -> float | str:
    """Project CGPA after adding a semester's GPA and credit hours."""
    if not _is_finite_number(current_cgpa) or not 0.0 <= current_cgpa <= 4.0:
        return "Error: current_cgpa must be a finite number between 0.0 and 4.0"
    if not _is_finite_number(semester_gpa) or not 0.0 <= semester_gpa <= 4.0:
        return "Error: semester_gpa must be a finite number between 0.0 and 4.0"
    if not _is_finite_number(completed_credit_hours) or completed_credit_hours < 0.0:
        return "Error: completed_credit_hours must be a finite non-negative number"
    if not _is_finite_number(semester_credit_hours) or semester_credit_hours <= 0.0:
        return "Error: semester_credit_hours must be a finite number greater than 0"

    total_credit_hours = completed_credit_hours + semester_credit_hours
    new_cgpa = (
        current_cgpa * completed_credit_hours
        + semester_gpa * semester_credit_hours
    ) / total_credit_hours
    return round(new_cgpa, 2)


def required_gpa_for_target(
    target_cgpa: float,
    current_cgpa: float,
    completed_credit_hours: float,
    remaining_credit_hours: float,
) -> float | str:
    """Calculate the average GPA needed over remaining credits to reach a target CGPA."""
    if not _is_finite_number(target_cgpa) or not 0.0 <= target_cgpa <= 4.0:
        return "Error: target_cgpa must be a finite number between 0.0 and 4.0"
    if not _is_finite_number(current_cgpa) or not 0.0 <= current_cgpa <= 4.0:
        return "Error: current_cgpa must be a finite number between 0.0 and 4.0"
    if not _is_finite_number(completed_credit_hours) or completed_credit_hours < 0.0:
        return "Error: completed_credit_hours must be a finite non-negative number"
    if not _is_finite_number(remaining_credit_hours) or remaining_credit_hours <= 0.0:
        return "Error: remaining_credit_hours must be a finite number greater than 0"

    total_credit_hours = completed_credit_hours + remaining_credit_hours
    required_gpa = (
        target_cgpa * total_credit_hours
        - current_cgpa * completed_credit_hours
    ) / remaining_credit_hours
    return round(required_gpa, 2)


def get_semester_courses(semester: int) -> str:
    """Return official course codes, titles, and credit hours for a semester (1-8)."""
    if type(semester) is not int or semester not in COURSES:
        return "Error: semester must be an integer between 1 and 8"

    course_list = COURSES[semester]
    lines = [f"Semester {semester} Courses:"]
    total_credit_hours = 0.0
    for code, title, credit in course_list:
        lines.append(f"{code}: {title} ({credit} credit hours)")
        total_credit_hours += credit
    lines.append(f"Total Credit Hours: {total_credit_hours}")
    return "\n".join(lines)


def get_remaining_credit_hours(current_semester: int) -> float | str:
    """Return graded credit hours remaining from the current semester through semester 8."""
    if type(current_semester) is not int or not 1 <= current_semester <= 8:
        return "Error: semester must be an integer between 1 and 8"

    remaining_credit_hours = sum(
        sum(credit for _, _, credit in COURSES[semester])
        for semester in range(current_semester, 9)
    )
    return round(remaining_credit_hours, 2)


def get_credit_hours(semesters: list[int]) -> float | str:
    """Return combined graded credit hours for a list of semesters (1-8)."""
    if not isinstance(semesters, list) or not semesters:
        return "Error: semesters must be a non-empty list of semester numbers (1 to 8)"

    total_credit_hours = 0.0
    for semester in semesters:
        if type(semester) is not int or not 1 <= semester <= 8:
            return f"Error: semester {semester} is invalid. Semesters must be integers between 1 and 8"
        total_credit_hours += sum(
            credit for _, _, credit in COURSES[semester]
        )
    return round(total_credit_hours, 2)


def save_report(filename: str, content: str) -> str:
    """Save a student-approved academic summary or GPA report as a text file."""
    if not filename or not filename.strip():
        return "Error: filename cannot be empty"
    if not content or not content.strip():
        return "Error: content cannot be empty"

    try:
        safe_filename = os.path.basename(filename.strip())
        if not safe_filename.endswith(".txt"):
            safe_filename += ".txt"
        with open(safe_filename, "w", encoding="utf-8") as report_file:
            report_file.write(content)
        return f"Report successfully saved to {safe_filename}"
    except OSError as exc:
        return f"Error: Could not save report: {exc}"
