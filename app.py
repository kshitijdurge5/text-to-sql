"""A small, dependency-free portfolio demonstration."""
import argparse
import csv
import json
import re
from pathlib import Path

PROJECT_KIND = "text_to_sql"
PROJECT_TITLE = "Natural Language to SQL Demo"


def words(text):
    return set(re.findall(r"[a-zA-Z0-9_]+", (text or "").lower()))


def run_demo(text="", data_path=None):
    text = (text or "").strip()

    if PROJECT_KIND == "agentic_workflow":
        tasks = [x.strip() for x in re.split(r"[;\n]", text) if x.strip()]
        if not tasks:
            tasks = ["Understand the goal", "Gather required information",
                     "Complete the work", "Review the result"]
        return {"project": PROJECT_TITLE, "workflow": [
            {"step": i, "task": task, "status": "planned"}
            for i, task in enumerate(tasks, 1)
        ], "note": "Planning demo; tasks are not executed automatically."}

    if PROJECT_KIND == "customer_support":
        rules = [
            (("refund", "payment", "charged", "billing"), "billing",
             "Please share your order reference and the charge details so the team can investigate."),
            (("password", "login", "sign in", "account"), "account access",
             "Try the official password-reset process. Never send anyone your password or OTP."),
            (("broken", "error", "bug", "not working"), "technical issue",
             "Please share the error message and the steps needed to reproduce the issue."),
            (("delivery", "shipping", "order"), "order status",
             "Please provide your order reference so the delivery status can be checked.")
        ]
        category, response = "general", "Thank you for contacting support. Please describe the issue and the outcome you need."
        for keys, label, answer in rules:
            if any(k in text.lower() for k in keys):
                category, response = label, answer
                break
        return {"project": PROJECT_TITLE, "category": category,
                "suggested_reply": response, "requires_human_review": True}

    if PROJECT_KIND == "data_analyst":
        sample = [
            {"product": "A", "sales": "120", "units": "4"},
            {"product": "B", "sales": "250", "units": "8"},
            {"product": "C", "sales": "180", "units": "6"}
        ]
        if data_path:
            with open(data_path, newline="", encoding="utf-8-sig") as f:
                rows = list(csv.DictReader(f))
        else:
            rows = sample
        if not rows:
            return {"project": PROJECT_TITLE, "rows": 0, "columns": [], "numeric_summary": {}}
        numeric = {}
        for col in rows[0]:
            values = []
            for row in rows:
                try:
                    values.append(float(row[col]))
                except (ValueError, TypeError, KeyError):
                    pass
            if values and len(values) == len(rows):
                numeric[col] = {"count": len(values), "sum": sum(values),
                                "mean": round(sum(values) / len(values), 2),
                                "min": min(values), "max": max(values)}
        return {"project": PROJECT_TITLE, "rows": len(rows),
                "columns": list(rows[0].keys()), "numeric_summary": numeric,
                "sample_rows": rows[:3]}

    if PROJECT_KIND == "email_assistant":
        goal = text or "Follow up on the pending task"
        return {"project": PROJECT_TITLE,
                "subject": "Follow-up: " + goal[:70],
                "email_draft": "Hello,\n\nI am writing to follow up regarding " + goal +
                    ". Could you please share an update when convenient?\n\nThank you.",
                "checklist": ["Confirm the recipient", "Verify names and dates",
                              "Review the draft before sending"]}

    if PROJECT_KIND == "invoice_processor":
        fields = {}
        for line in text.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                key = re.sub(r"[^a-zA-Z0-9_ ]", "", key).strip().lower().replace(" ", "_")
                if key:
                    fields[key] = value.strip()
        amount = fields.get("total", fields.get("amount", ""))
        return {"project": PROJECT_TITLE, "extracted_fields": fields,
                "amount_found": amount or None,
                "missing_common_fields": [k for k in ("invoice_number", "date", "vendor", "total")
                    if k not in fields],
                "note": "Verify extracted values against the original invoice."}

    if PROJECT_KIND == "multi_agent":
        query = text or "Research a topic"
        return {"project": PROJECT_TITLE, "query": query,
                "pipeline": [
                    {"agent": "Planner", "task": "Break the question into subquestions"},
                    {"agent": "Researcher", "task": "Collect sources for each subquestion"},
                    {"agent": "Verifier", "task": "Check source quality and conflicting evidence"},
                    {"agent": "Writer", "task": "Prepare a cited summary"}
                ],
                "demo_note": "This is a simulated multi-agent plan; no web research was performed."}

    if PROJECT_KIND == "rag_chatbot":
        documents = [
            ("getting_started.txt", "Install Python, create a virtual environment, and run the application."),
            ("security.txt", "Never commit API keys, passwords, access tokens, or personal information."),
            ("testing.txt", "Run the automated tests before making changes or publishing a release.")
        ]
        query_words = words(text)
        ranked = []
        for name, content in documents:
            overlap = len(query_words & words(content))
            if overlap:
                ranked.append({"document": name, "score": overlap, "text": content})
        ranked.sort(key=lambda item: item["score"], reverse=True)
        return {"project": PROJECT_TITLE, "question": text,
                "retrieved_documents": ranked[:3],
                "answer": " ".join(item["text"] for item in ranked[:3]) or
                    "No matching local document was found. Add documents and try again.",
                "note": "Keyword retrieval demo; it does not use embeddings or an LLM."}

    if PROJECT_KIND == "fact_checker":
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        claim = lines[0] if lines else "Enter a claim to investigate."
        evidence = lines[1:] if len(lines) > 1 else []
        return {"project": PROJECT_TITLE, "claim": claim, "provided_evidence": evidence,
                "status": "UNVERIFIED",
                "next_steps": ["Find reliable primary sources",
                    "Check publication date and context",
                    "Seek independent corroboration",
                    "Record evidence against and in favour"],
                "note": "The tool does not independently establish whether a claim is true."}

    if PROJECT_KIND == "resume_matcher":
        resume, job = (text.split("\n---JOB---", 1) + [""])[:2]
        if not job:
            job = "Python SQL data analysis communication problem solving"
        a, b = words(resume), words(job)
        matched = sorted(a & b)
        missing = sorted(b - a)
        return {"project": PROJECT_TITLE, "matched_keywords": matched,
                "missing_keywords": missing, "match_percentage": round(100 * len(matched) / max(1, len(b)), 1),
                "note": "A basic keyword comparison, not a hiring decision. Use truthful resume details."}

    if PROJECT_KIND == "text_to_sql":
        q = text.lower()
        if "count" in q or "how many" in q:
            sql = "SELECT COUNT(*) FROM customers;"
        elif "average" in q or "avg" in q:
            sql = "SELECT AVG(amount) FROM orders;"
        elif "top" in q or "highest" in q:
            sql = "SELECT * FROM orders ORDER BY amount DESC LIMIT 10;"
        elif "customer" in q:
            sql = "SELECT * FROM customers LIMIT 100;"
        else:
            sql = "SELECT * FROM orders LIMIT 100;"
        return {"project": PROJECT_TITLE, "request": text,
                "example_sql": sql,
                "warning": "Illustrative SQL only. Check table and column names before use; this program does not execute SQL."}

    return {"project": PROJECT_TITLE, "message": "Unknown project type."}


def main():
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--input", "-i", default="", help="Text or question for the demo")
    parser.add_argument("--data", default=None, help="Optional CSV file (data analyst project)")
    args = parser.parse_args()
    try:
        result = run_demo(args.input, args.data)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except (OSError, csv.Error, UnicodeError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
