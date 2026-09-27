import sys, json
from client import PersonalInboxCognitiveTriage

def main():
    triage = PersonalInboxCognitiveTriage()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(triage.run_benchmark_inbox_triage(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            params = req.get("params", {})
            rid = req.get("id")

            if method == "tools/list":
                res = {
                    "tools": [
                        {"name": "triage_message", "description": "Classify message urgency and required effort."},
                        {"name": "generate_action_queue", "description": "Sort pending messages into quick-hits vs deep focus."},
                        {"name": "estimate_cognitive_effort", "description": "Estimate reading and reply duration in minutes."},
                        {"name": "run_benchmark_inbox_triage", "description": "Run inbox triage benchmark."}
                    ]
                }
            elif method == "tools/call":
                tname = params.get("name")
                args = params.get("arguments", {})
                if tname == "triage_message":
                    out = triage.triage_message(args.get("sender", ""), args.get("subject", ""), args.get("body", ""), args.get("sender_vip_score", 0.5))
                elif tname == "generate_action_queue":
                    out = triage.generate_action_queue(args.get("messages", []))
                elif tname == "estimate_cognitive_effort":
                    out = triage.estimate_cognitive_effort(args.get("subject", ""), args.get("body", ""))
                elif tname == "run_benchmark_inbox_triage":
                    out = triage.run_benchmark_inbox_triage()
                else:
                    out = {"error": f"Unknown tool {tname}"}
                res = {"content": [{"type": "text", "text": json.dumps(out)}]}
            else:
                res = {"error": "Unsupported method"}
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": res}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    main()
