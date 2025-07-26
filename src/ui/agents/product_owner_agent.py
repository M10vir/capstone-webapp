def review_solution(plan: str, code: str) -> dict:
    """Review Software Engineer's plan and code for approval."""
    is_html_formatted = "```html" in code and code.strip().endswith("```")
    checks_passed = all([
        "argparse" in code,
        "def add" in code,
        "def divide" in code,
        "Error: Divide by zero" in code
    ])

    approved = is_html_formatted and checks_passed
    comments = []
    if not is_html_formatted:
        comments.append("Code block missing required ```html formatting.")
    if not checks_passed:
        comments.append("Some arithmetic logic  or error handling may be incomplete.")
    if approved:
        comments.append("READY FOR USER APPROVAL")

    return {
        "approved": approved, 
        "comments": " ".join(comments) or "Reviewed."
    }
