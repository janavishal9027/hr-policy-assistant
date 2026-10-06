""""""

POLICY_DICTIONARY = {
    "leave": [
        "leave",
        "annual leave",
        "sick leave",
        "paid leave",
        "vacation",
        "medical certificate",
    ],

    "work_from_home": [
        "work from home",
        "wfh",
        "remote work",
        "remote",
        "home working",
    ],

    "probation": [
        "probation",
        "probation period",
        "new employee",
    ],

    "notice_period": [
        "notice period",
        "resignation",
        "notice",
        "last working day",
    ],

    "reimbursement": [
        "reimbursement",
        "expense claim",
        "business expense",
    ],

    "code_of_conduct": [
        "code of conduct",
        "misconduct",
        "harassment",
        "disciplinary",
    ],

    "holidays": [
        "holiday",
        "public holiday",
        "compensatory leave",
    ],

    "exit": [
        "exit",
        "separation",
        "clearance",
        "full and final",
    ],

    "attendance": [
        "attendance",
        "late arrival",
        "absence",
        "punctuality",
    ],

    "working_hours": [
        "working hours",
        "overtime",
        "working schedule",
    ],

    "benefits": [
        "benefits",
        "health insurance",
        "life insurance",
        "retirement benefits",
    ],

    "performance": [
        "performance",
        "performance review",
        "PIP",
        "performance improvement plan",
    ],

    "promotion": [
        "promotion",
        "career development",
        "internal mobility",
    ],

    "training": [
        "training",
        "certification",
        "learning",
    ],

    "recruitment": [
        "recruitment",
        "hiring",
        "candidate",
        "job description",
    ],

    "onboarding": [
        "onboarding",
        "joining",
        "new employee",
    ],

    "transfer": [
        "transfer",
        "relocation",
        "internal transfer",
    ],

    "expense": [
        "expense",
        "expense management",
        "receipts",
        "invoice",
    ],

    "records_retention": [
        "records retention",
        "retention",
        "record",
        "legal hold",
        "records preservation",
    ],

    "it_acceptable_use": [
        "IT",
        "acceptable use",
        "password",
        "security",
        "software installation",
        "phishing",
    ],
}


def identify_policy(question: str):
    """
    Identify likely HR policy categories from the user's question.
    """

    question_lower = question.lower()

    matched_policies = []

    for policy, keywords in POLICY_DICTIONARY.items():

        for keyword in keywords:

            if keyword.lower() in question_lower:

                matched_policies.append(policy)

                break

    return matched_policies