import sys, json
from client import PersonalInboxCognitiveTriage

def main():
    print("Testing PersonalInboxCognitiveTriage...")
    triage = PersonalInboxCognitiveTriage()
    res = triage.run_benchmark_inbox_triage()
    print(json.dumps(res, indent=2))
    assert res["benchmark_status"] == "PASSED"
    assert res["top_priority_action"] == "IMMEDIATE_ACTION"
    assert res["newsletter_action"] == "AUTO_ARCHIVE_OR_DIGEST"
    print("All Personal Inbox Cognitive Triage tests passed successfully!")

if __name__ == "__main__":
    main()
