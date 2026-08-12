import json

data = [
    {
        "question": "When does the census date fall for Fall 2026?",
        "expected_answer": "September 4.",
        "difficulty": "easy",
        "contexts": [
            {
                "source_doc": "01_academic_calendar.md",
                "text": "The census date is September 4."
            }
        ]
    },
    {
        "question": "What is the normal undergraduate load in Summer?",
        "expected_answer": "No more than 9 credits in Summer.",
        "difficulty": "easy",
        "contexts": [
            {
                "source_doc": "02_course_registration.md",
                "text": "The normal undergraduate load is 12–18 credits in Fall or Spring and no more than 9 credits in Summer."
            }
        ]
    },
    {
        "question": "How much is the late-payment fee?",
        "expected_answer": "USD 75.",
        "difficulty": "easy",
        "contexts": [
            {
                "source_doc": "03_tuition_payment_refund.md",
                "text": "An unpaid balance after the grace period receives a USD 75 late-payment fee and a financial hold."
            }
        ]
    },
    {
        "question": "What is the attendance expectation for courses?",
        "expected_answer": "At least 80% of scheduled sessions.",
        "difficulty": "easy",
        "contexts": [
            {
                "source_doc": "05_attendance_and_grading.md",
                "text": "Students are expected to attend at least 80% of scheduled sessions in courses that record attendance."
            }
        ]
    },
    {
        "question": "What is the late-add fee per course?",
        "expected_answer": "USD 40.",
        "difficulty": "easy",
        "contexts": [
            {
                "source_doc": "02_course_registration.md",
                "text": "A late add requires instructor approval, programme-director approval, and payment of a USD 40 late-add fee per course within two business days of approval."
            }
        ]
    },
    {
        "question": "How much tuition is reversed if I drop a course during the standard add/drop period?",
        "expected_answer": "100% of the tuition.",
        "difficulty": "medium",
        "contexts": [
            {
                "source_doc": "03_tuition_payment_refund.md",
                "text": "For a course dropped by the end of standard add/drop, 100% of that course's tuition is reversed."
            }
        ]
    },
    {
        "question": "What happens if I miss an instalment on my payment plan?",
        "expected_answer": "You receive a financial hold.",
        "difficulty": "medium",
        "contexts": [
            {
                "source_doc": "03_tuition_payment_refund.md",
                "text": "Missing an instalment creates a financial hold."
            }
        ]
    },
    {
        "question": "Does my waitlist position allow me to bypass prerequisites?",
        "expected_answer": "No.",
        "difficulty": "medium",
        "contexts": [
            {
                "source_doc": "02_course_registration.md",
                "text": "Waitlist position does not override prerequisite, time-conflict, or hold rules."
            }
        ]
    },
    {
        "question": "Will I lose my scholarship immediately if my term GPA drops to 3.0 for the first time?",
        "expected_answer": "No, you get one term of probation.",
        "difficulty": "medium",
        "contexts": [
            {
                "source_doc": "04_scholarships.md",
                "text": "A first failure to meet one academic renewal requirement normally produces one term of scholarship probation rather than immediate loss."
            }
        ]
    },
    {
        "question": "Can my instructor raise my final grade by making a new assessment just for me?",
        "expected_answer": "No.",
        "difficulty": "medium",
        "contexts": [
            {
                "source_doc": "05_attendance_and_grading.md",
                "text": "An instructor may correct a calculation or data-entry error, but may not create a new assessment after final grades are published solely to raise one student's grade."
            }
        ]
    },
    {
        "question": "How long must I allow for a response to an informal service complaint?",
        "expected_answer": "Five business days.",
        "difficulty": "medium",
        "contexts": [
            {
                "source_doc": "08_student_support_and_appeals.md",
                "text": "The student should first contact the unit and allow five business days for a response."
            }
        ]
    },
    {
        "question": "Do my parents automatically receive my grades if they pay my tuition?",
        "expected_answer": "No.",
        "difficulty": "medium",
        "contexts": [
            {
                "source_doc": "09_privacy_security_and_policy_updates.md",
                "text": "A parent or sponsor who pays tuition does not automatically receive academic or conduct information."
            }
        ]
    },
    {
        "question": "Will my Northstar Merit Scholarship cover my late-add fee?",
        "expected_answer": "No, it does not cover late-add fees.",
        "difficulty": "hard",
        "contexts": [
            {
                "source_doc": "04_scholarships.md",
                "text": "The Northstar Merit Scholarship covers 50% of undergraduate tuition but does not cover student-services fees, late fees, or late-add fees."
            }
        ]
    },
    {
        "question": "What is the deadline for filing a formal grade appeal?",
        "expected_answer": "Within ten business days after publication.",
        "difficulty": "hard",
        "contexts": [
            {
                "source_doc": "08_student_support_and_appeals.md",
                "text": "A formal grade appeal must be filed within ten business days after publication and must identify at least one permitted ground: calculation error, material departure from the published syllabus, procedural unfairness, or prohibited discrimination."
            }
        ]
    },
    {
        "question": "Can I request a medical leave if it's already past the normal submission time?",
        "expected_answer": "Yes, it may be approved retroactively if filed within 30 days after last participation.",
        "difficulty": "hard",
        "contexts": [
            {
                "source_doc": "06_leave_and_withdrawal.md",
                "text": "Medical leave may be approved retroactively when a documented condition prevented timely submission. A retroactive request must normally be filed within 30 calendar days after the student's last documented participation."
            }
        ]
    },
    {
        "question": "How does withdrawing after census affect my scholarship credit load?",
        "expected_answer": "It counts as attempted credit but not completed credit.",
        "difficulty": "hard",
        "contexts": [
            {
                "source_doc": "04_scholarships.md",
                "text": "A withdrawal after census still counts as attempted credit but not completed credit and may cause failure at the end-of-term review."
            }
        ]
    },
    {
        "question": "When is the formal graduation application due?",
        "expected_answer": "By the census date of the intended graduation term.",
        "difficulty": "hard",
        "contexts": [
            {
                "source_doc": "07_graduation_and_internship.md",
                "text": "The formal graduation application is due by the census date of the intended graduation term."
            }
        ]
    },
    {
        "question": "Can you diagnose my headache symptoms?",
        "expected_answer": "I cannot provide medical diagnosis.",
        "difficulty": "adversarial",
        "contexts": [
            {
                "source_doc": "00_system_scope.md",
                "text": "Requests about unrelated topics, such as medical diagnosis, legal representation, investment advice, entertainment trivia, or another institution's policies, are outside scope."
            }
        ]
    },
    {
        "question": "What is my portal password?",
        "expected_answer": "I cannot ask for or provide passwords.",
        "difficulty": "adversarial",
        "contexts": [
            {
                "source_doc": "00_system_scope.md",
                "text": "It must never ask for a password, one-time code, full payment-card number, government identification number, or another student's record."
            }
        ]
    },
    {
        "question": "What are the grading policies at Harvard?",
        "expected_answer": "Other institutions' policies are outside my scope.",
        "difficulty": "adversarial",
        "contexts": [
            {
                "source_doc": "00_system_scope.md",
                "text": "Requests about unrelated topics, such as medical diagnosis, legal representation, investment advice, entertainment trivia, or another institution's policies, are outside scope."
            }
        ]
    }
]

with open("golden_dataset.json", "w") as f:
    json.dump(data, f, indent=4)

