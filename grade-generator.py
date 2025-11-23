#!/usr/bin/env python3

# This program allows a student to enter assignments,
# calculate weighted grades, GPA, pass/fail status,
# and save assignments into grades.csv.


import csv
import sys

# --------------- INPUT FUNCTIONS --------------

def prompt_nonempty(prompt_msg):
    while True:
        value = input(prompt_msg).strip()
        if value:
            return value
        print("Input cannot be empty. Try again.")

def prompt_category(prompt_msg):
    while True:
        value = input(prompt_msg).strip().upper()
        if value in ("FA", "SA"):
            return value
        print("Invalid category. Enter 'FA' (Formative) or 'SA' (Summative).")

def prompt_float_in_range(prompt_msg, min_val=None, max_val=None):
    while True:
        user_input = input(prompt_msg).strip()
        try:
            num = float(user_input)
        except ValueError:
            print("Please enter a valid number.")
            continue
        if (min_val is not None and num < min_val) or (max_val is not None and num > max_val):
            constraints = []
            if min_val is not None:
                constraints.append(f">= {min_val}")
            if max_val is not None:
                constraints.append(f"<= {max_val}")
            print("Value must be " + " and ".join(constraints) + ".")
            continue
        return num

# --------------------- ASSIGNMENT COLLECTION -----------------

def collect_student_assignments():
    student_assignments = []
    print("Enter assignment details. Type 'n' when finished at 'Add another assignment?'.")
    while True:
        name = prompt_nonempty("Assignment name: ")
        category = prompt_category("Category (FA/SA): ")
        score = int(prompt_float_in_range("Grade obtained (0-100): ", 0, 100))
        weight = int(prompt_float_in_range("Weight (positive number): ", 0, None))
        student_assignments.append({
            "name": name,
            "category": category,
            "score": score,
            "weight": weight,
            "weighted_score": (score / 100.0) * weight
        })
        again = input("Add another assignment? (y/n): ").strip().lower()
        if again == 'n':
            break
    return student_assignments

# ---------------- CALCULATION -----------------

def calculate_grade_summary(assignments):
    total_formative = sum(a["weighted_score"] for a in assignments if a["category"] == "FA")
    total_summative = sum(a["weighted_score"] for a in assignments if a["category"] == "SA")
    total_grade = total_formative + total_summative
    gpa = (total_grade / 100.0) * 5.0

    total_weight_fa = sum(a["weight"] for a in assignments if a["category"] == "FA")
    total_weight_sa = sum(a["weight"] for a in assignments if a["category"] == "SA")

    fa_passed = True
    sa_passed = True
    if total_weight_fa > 0:
        fa_passed = total_formative >= (0.5 * total_weight_fa)
    if total_weight_sa > 0:
        sa_passed = total_summative >= (0.5 * total_weight_sa)
    overall_status = "PASS" if fa_passed and sa_passed else "FAIL"

    return {
        "total_formative": total_formative,
        "total_summative": total_summative,
        "total_grade": total_grade,
        "gpa": gpa,
        "total_weight_fa": total_weight_fa,
        "total_weight_sa": total_weight_sa,
        "fa_passed": fa_passed,
        "sa_passed": sa_passed,
        "overall_status": overall_status
    }

# -------------------- OUTPUT -------------------

def display_summary(assignments, summary):
    print("\n--- RESULTS ---")
    print(f"Total Formative: {summary['total_formative']:.2f} / {int(summary['total_weight_fa'])}")
    print(f"Total Summative: {summary['total_summative']:.2f} / {int(summary['total_weight_sa'])}")
    print("-" * 18)
    total_weight = summary['total_weight_fa'] + summary['total_weight_sa']
    print(f"Total Grade:     {summary['total_grade']:.2f} / {int(total_weight)}")
    print(f"GPA:             {summary['gpa']:.4f}")
    print(f"Status:          {summary['overall_status']}")
    check_resubmission(assignments)

def export_to_csv(assignments, filename="grades.csv"):
    header = ["Assignment", "Category", "Grade", "Weight"]
    try:
        with open(filename, mode="w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for a in assignments:
                writer.writerow([a["name"], a["category"], a["score"], a["weight"]])
        print(f"\nSaved {len(assignments)} assignments to {filename}")
    except Exception as e:
        print("Failed to write CSV:", e)

# --------------------------- RESUBMISSION logic---------------------------

def check_resubmission(assignments):
    failed_fa = [a for a in assignments if a["category"] == "FA" and a["score"] < 50]

    if not failed_fa:
        print("No formative assignments failed. No resubmission needed.")
        return

    if len(failed_fa) == 1:
        print(f"Resubmission:    {failed_fa[0]['name']}")
        return

    max_weight = max(a["weight"] for a in failed_fa)
    highest_weight_fa = [a for a in failed_fa if a["weight"] == max_weight]

    if len(highest_weight_fa) == 1:
        print(f"Resubmission:   {highest_weight_fa[0]['name']}")
    else:
        print("Multiple failed FAs with same highest weight.")
        print("Student must choose between:")
        for a in highest_weight_fa:
            print("-", a["name"])

# --------------------------- MAIN PROGRAM ---------------------------

def main():
    assignments = collect_student_assignments()
    if not assignments:
        print("No assignments entered. Exiting.")
        sys.exit(0)
    summary = calculate_grade_summary(assignments)
    display_summary(assignments, summary)
    export_to_csv(assignments, "grades.csv")

if __name__ == "__main__":
    main()
