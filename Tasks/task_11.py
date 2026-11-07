''' Task 11 | Multi-File Student Gradebook
Concepts: File handling, dictionaries, exceptions
Problem: Merge students.csv (student_id,name) and scores.csv (student_id,subject,marks). Calculate per-student average, grade, and rank; export report.csv.
Requirements: Marks must be 0–100; reject unknown IDs and duplicate student-subject entries. Grades: A>=85, B>=70, C>=55, D>=40, otherwise F. Rank by average, then ID.
Sample / expected behavior: Student 101 with marks 90,80,85 -> average 85.0, grade A.'''



import csv


def create_sample_files():
    students_data = [
        ["student_id", "name"],
        ["S01", "Ali"],
        ["S02", "Sara"],
        ["S03", "Ahmed"],
        ["S04", "Usman"]
    ]

    scores_data = [
        ["student_id", "subject", "marks"],
        ["S01", "Python", 90],
        ["S01", "SQL", 80],
        ["S02", "Python", 95],
        ["S02", "SQL", 85],
        ["S03", "Python", 60],
        ["S03", "SQL", 70],
        ["S04", "Python", 35],
        ["S04", "SQL", 45],
        ["S01", "Python", 100]
    ]

    with open("students.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(students_data)

    with open("scores.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(scores_data)


def calculate_grade(average):
    if average >= 85:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 55:
        return "C"
    elif average >= 40:
        return "D"
    else:
        return "F"


def generate_gradebook(students_file, scores_file):
    students = {}

   
    with open(students_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            student_id = row["student_id"].strip()
            name = row["name"].strip()

            if not student_id or not name:
                raise ValueError("Student ID and name cannot be empty")

            if student_id in students:
                raise ValueError("Duplicate student ID: " + student_id)

            students[student_id] = {
                "name": name,
                "marks": [],
                "subjects": set()
            }

    rejected_scores = []

   
    with open(scores_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            student_id = row["student_id"].strip()
            subject = row["subject"].strip()

            try:
                marks = float(row["marks"])
            except (ValueError, TypeError):
                rejected_scores.append({
                    "student_id": student_id,
                    "subject": subject,
                    "reason": "Invalid marks"
                })
                continue

            if student_id not in students:
                reason = "Unknown student ID"

            elif not subject:
                reason = "Subject cannot be empty"

            elif not 0 <= marks <= 100:
                reason = "Marks must be between 0 and 100"

            elif subject in students[student_id]["subjects"]:
                reason = "Duplicate student-subject record"

            else:
                reason = None

            if reason is not None:
                rejected_scores.append({
                    "student_id": student_id,
                    "subject": subject,
                    "reason": reason
                })
                continue

            students[student_id]["marks"].append(marks)
            students[student_id]["subjects"].add(subject)

 
    report = []

    for student_id, details in students.items():
        if len(details["marks"]) == 0:
            average = 0
        else:
            average = sum(details["marks"]) / len(details["marks"])

        grade = calculate_grade(average)

        report.append({
            "student_id": student_id,
            "name": details["name"],
            "average": round(average, 2),
            "grade": grade
        })

  
    report.sort(key=lambda student: (
        -student["average"],
        student["student_id"]
    ))

  
    for rank, student in enumerate(report, start=1):
        student["rank"] = rank

   
    with open("report.csv", "w", newline="", encoding="utf-8") as file:
        fieldnames = ["student_id", "name", "average", "grade", "rank"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(report)

    return report, rejected_scores



create_sample_files()


report, rejected_scores = generate_gradebook(
    "students.csv",
    "scores.csv"
)

print("STUDENT GRADEBOOK REPORT")
print("-" * 60)

for student in report:
    print(student)

print("\nREJECTED SCORES")
print("-" * 60)

for rejected in rejected_scores:
    print(rejected)

print("\nSUMMARY")
print("-" * 60)
print("Total students:", len(report))
print("Rejected scores:", len(rejected_scores))
print("Report file created: report.csv")
