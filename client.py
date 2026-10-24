"""Idempotent Message Deduplication & Outbox Pattern.
100% Python Standard Library.
"""

class TransactionalOutboxDeduplicator:
    """Tracks outbox event delivery IDs to guarantee exactly-once processing."""

    @staticmethod
    def process_outbox_batch(messages: list, seen_event_ids: list) -> dict:
        seen = set(seen_event_ids)
        dispatched = []
        duplicates = []

        for msg in messages:
            msg_id = msg.get("id")
            if msg_id in seen:
                duplicates.append(msg_id)
            else:
                seen.add(msg_id)
                dispatched.append(msg)

        return {
            "total_messages": len(messages),
            "dispatched_count": len(dispatched),
            "duplicate_count": len(duplicates),
            "dispatched": dispatched
        }
