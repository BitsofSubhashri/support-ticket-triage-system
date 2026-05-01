import pandas as pd
import os

# 🔹 Classify ticket
def classify_ticket(text):
    text = text.lower()

    if any(word in text for word in ["login","password","signin"]):
        return "login_issue"

    elif any(word in text for word in ["payment","charged","refund","billing"]):
        return "billing_issue"

    elif any(word in text for word in ["error","bug","crash","not working","fail"]):
        return "bug_report"

    elif any(word in text for word in ["fraud","unauthorized","hacked","scam"]):
        return "fraud"

    elif any(word in text for word in ["access","permission","denied"]):
        return "account_access"

    return "general_query"


# 🔹 Escalation logic
def should_escalate(category, text):
    text = text.lower()

    if category in ["fraud", "billing_issue"]:
        return True

    if "urgent" in text or "asap" in text:
        return True

    return False


# 🔹 Response generator (domain-aware)
def generate_response(category, escalate, domain):
    if escalate:
        return f"This issue is sensitive and has been escalated to {domain} support."

    responses = {
        "login_issue": f"Please reset your password via {domain} help center.",
        "billing_issue": f"Check your billing section on {domain} or contact support.",
        "bug_report": f"{domain} team is working on resolving this issue.",
        "account_access": f"Please verify permissions or contact {domain} admin support.",
        "general_query": f"Please visit {domain} help center for more details."
    }

    return responses.get(category, "We will get back to you shortly.")


# 🔹 Main processing function
def process_tickets():
    df = pd.read_csv("../data/support_tickets.csv")

    results = []

    # clear old log
    open("../output/log.txt", "w").close()

    for i, row in df.iterrows():
        ticket_id = i

        # combine fields for better understanding
        text = str(row["Issue"]) + " " + str(row["Subject"])
        company = str(row["Company"])

        # 🔹 Domain classification
        if "hacker" in company.lower():
            domain = "hackerrank"
        elif "claude" in company.lower():
            domain = "claude"
        elif "visa" in company.lower():
            domain = "visa"
        else:
            domain = "general"

        # 🔹 Core logic
        category = classify_ticket(text)
        escalate = should_escalate(category, text)
        response = generate_response(category, escalate, domain)

        # 🔹 Save result
        results.append([ticket_id, domain, category, escalate, response])

        # 🔹 Logging (IMPORTANT for transcript)
        with open("../output/log.txt", "a") as f:
            f.write(f"{ticket_id} | {domain} | {category} | {escalate}\n")

    # 🔹 Output CSV
    output_df = pd.DataFrame(
        results,
        columns=["ticket_id", "domain", "category", "escalate", "response"]
    )

    output_df.to_csv("../output/output.csv", index=False)

    print("✅ Done! Output + log generated.")


# 🔹 Run
if __name__ == "__main__":
    process_tickets()