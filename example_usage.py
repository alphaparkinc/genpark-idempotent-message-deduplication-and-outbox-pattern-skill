"""Example usage for Transactional Outbox Deduplicator."""
from client import TransactionalOutboxDeduplicator

if __name__ == "__main__":
    res = TransactionalOutboxDeduplicator.process_outbox_batch(
        [{"id": "msg_1"}, {"id": "msg_2"}, {"id": "msg_1"}],
        ["msg_0"]
    )
    print("Dispatched Count:", res["dispatched_count"], "Duplicates:", res["duplicate_count"])
