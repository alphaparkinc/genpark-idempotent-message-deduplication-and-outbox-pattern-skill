"""MCP server for Transactional Outbox Deduplicator."""
import sys
import json
from client import TransactionalOutboxDeduplicator

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [{
                "name": "process_transactional_outbox",
                "description": "Filters out duplicate event IDs and returns freshly dispatched messages",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "messages": {"type": "array"},
                        "seen_event_ids": {"type": "array"}
                    },
                    "required": ["messages", "seen_event_ids"]
                }
            }]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        if params.get("name") == "process_transactional_outbox":
            args = params.get("arguments", {})
            res = TransactionalOutboxDeduplicator.process_outbox_batch(
                args.get("messages", []),
                args.get("seen_event_ids", [])
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
