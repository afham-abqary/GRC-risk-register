import csv
import json
import os
from datetime import datetime

RISK_FILE = "risks.json"
REPORT_FILE = "risk_report.csv"

LIKELIHOOD_SCALE = {
    1: "Rare",
    2: "Unlikely",
    3: "Possible",
    4: "Likely",
    5: "Almost Certain"
}

IMPACT_SCALE = {
    1: "Negligible",
    2: "Minor",
    3: "Moderate",
    4: "Major",
    5: "Critical"
}

RISK_LEVEL = {
    range(1, 5): "Low",
    range(5, 10): "Medium",
    range(10, 16): "High",
    range(16, 26): "Critical"
}

def get_risk_level(score):
    for r, level in RISK_LEVEL.items():
        if score in r:
            return level
    return "Critical"

def load_risks():
    if os.path.exists(RISK_FILE):
        with open(RISK_FILE, "r") as f:
            return json.load(f)
    return []

def save_risks(risks):
    with open(RISK_FILE, "w") as f:
        json.dump(risks, f, indent=2)

def add_risk(risks):
    print("\n--- Add New Risk ---")
    risk_id = f"RISK-{len(risks) + 1:03d}"
    name = input("Risk name: ").strip()
    description = input("Description: ").strip()
    category = input("Category (e.g. Network, Application, Data, Access): ").strip()
    owner = input("Risk owner: ").strip()

    print("\nLikelihood scale: 1=Rare, 2=Unlikely, 3=Possible, 4=Likely, 5=Almost Certain")
    while True:
        try:
            likelihood = int(input("Likelihood (1-5): "))
            if 1 <= likelihood <= 5:
                break
            print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input.")

    print("\nImpact scale: 1=Negligible, 2=Minor, 3=Moderate, 4=Major, 5=Critical")
    while True:
        try:
            impact = int(input("Impact (1-5): "))
            if 1 <= impact <= 5:
                break
            print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input.")

    score = likelihood * impact
    level = get_risk_level(score)

    treatment = input("Treatment (Accept / Mitigate / Transfer / Avoid): ").strip()
    mitigation = input("Mitigation plan: ").strip()
    status = input("Status (Open / In Progress / Closed): ").strip()

    risk = {
        "id": risk_id,
        "name": name,
        "description": description,
        "category": category,
        "owner": owner,
        "likelihood": likelihood,
        "likelihood_label": LIKELIHOOD_SCALE[likelihood],
        "impact": impact,
        "impact_label": IMPACT_SCALE[impact],
        "risk_score": score,
        "risk_level": level,
        "treatment": treatment,
        "mitigation": mitigation,
        "status": status,
        "date_added": datetime.now().strftime("%Y-%m-%d"),
        "last_updated": datetime.now().strftime("%Y-%m-%d")
    }

    risks.append(risk)
    save_risks(risks)
    print(f"\nRisk {risk_id} added successfully. Risk Level: {level} (Score: {score})")

def view_risks(risks):
    if not risks:
        print("\nNo risks found.")
        return

    print("\n--- Risk Register ---")
    print(f"{'ID':<12} {'Name':<30} {'Level':<10} {'Score':<8} {'Status':<15} {'Owner'}")
    print("-" * 90)
    for r in risks:
        print(f"{r['id']:<12} {r['name'][:28]:<30} {r['risk_level']:<10} {r['risk_score']:<8} {r['status']:<15} {r['owner']}")

def view_risk_detail(risks):
    risk_id = input("\nEnter Risk ID (e.g. RISK-001): ").strip()
    risk = next((r for r in risks if r["id"] == risk_id), None)
    if not risk:
        print("Risk not found.")
        return

    print(f"\n--- {risk['id']}: {risk['name']} ---")
    print(f"Description   : {risk['description']}")
    print(f"Category      : {risk['category']}")
    print(f"Owner         : {risk['owner']}")
    print(f"Likelihood    : {risk['likelihood']} - {risk['likelihood_label']}")
    print(f"Impact        : {risk['impact']} - {risk['impact_label']}")
    print(f"Risk Score    : {risk['risk_score']}")
    print(f"Risk Level    : {risk['risk_level']}")
    print(f"Treatment     : {risk['treatment']}")
    print(f"Mitigation    : {risk['mitigation']}")
    print(f"Status        : {risk['status']}")
    print(f"Date Added    : {risk['date_added']}")
    print(f"Last Updated  : {risk['last_updated']}")

def update_risk(risks):
    risk_id = input("\nEnter Risk ID to update: ").strip()
    risk = next((r for r in risks if r["id"] == risk_id), None)
    if not risk:
        print("Risk not found.")
        return

    print(f"\nUpdating {risk_id}: {risk['name']}")
    print("Press Enter to keep current value.")

    new_status = input(f"Status [{risk['status']}]: ").strip()
    if new_status:
        risk["status"] = new_status

    new_mitigation = input(f"Mitigation [{risk['mitigation']}]: ").strip()
    if new_mitigation:
        risk["mitigation"] = new_mitigation

    new_treatment = input(f"Treatment [{risk['treatment']}]: ").strip()
    if new_treatment:
        risk["treatment"] = new_treatment

    risk["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    save_risks(risks)
    print(f"Risk {risk_id} updated successfully.")

def generate_report(risks):
    if not risks:
        print("\nNo risks to export.")
        return

    with open(REPORT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "id", "name", "description", "category", "owner",
            "likelihood", "likelihood_label", "impact", "impact_label",
            "risk_score", "risk_level", "treatment", "mitigation",
            "status", "date_added", "last_updated"
        ])
        writer.writeheader()
        writer.writerows(risks)

    print(f"\nReport exported to {REPORT_FILE} ({len(risks)} risks)")

def risk_summary(risks):
    if not risks:
        print("\nNo risks found.")
        return

    levels = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    statuses = {"Open": 0, "In Progress": 0, "Closed": 0}

    for r in risks:
        if r["risk_level"] in levels:
            levels[r["risk_level"]] += 1
        if r["status"] in statuses:
            statuses[r["status"]] += 1

    print("\n--- Risk Summary ---")
    print(f"Total Risks: {len(risks)}")
    print("\nBy Risk Level:")
    for level, count in levels.items():
        bar = "#" * count
        print(f"  {level:<10}: {bar} ({count})")
    print("\nBy Status:")
    for status, count in statuses.items():
        bar = "#" * count
        print(f"  {status:<12}: {bar} ({count})")

def main():
    print("GRC Risk Register - ISO/IEC 27001 Aligned")

    risks = load_risks()

    while True:
        print("\n--- Main Menu ---")
        print("1. Add new risk")
        print("2. View all risks")
        print("3. View risk detail")
        print("4. Update risk")
        print("5. Risk summary")
        print("6. Export report to CSV")
        print("7. Exit")

        choice = input("\nSelect option: ").strip()

        if choice == "1":
            add_risk(risks)
        elif choice == "2":
            view_risks(risks)
        elif choice == "3":
            view_risk_detail(risks)
        elif choice == "4":
            update_risk(risks)
        elif choice == "5":
            risk_summary(risks)
        elif choice == "6":
            generate_report(risks)
        elif choice == "7":
            print("\nGoodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
