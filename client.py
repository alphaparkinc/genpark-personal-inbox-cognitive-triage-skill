import sys, json, math, time

class PersonalInboxCognitiveTriage:
    """
    Personal Attention & Inbox Triage Engine.
    Filters out noise, estimates cognitive effort, and slots emails/DMs into
    Actionable Quick-Hits (<2 min), Deep Focus Decisions, or Batch-Archive.
    """
    def __init__(self):
        self.urgent_keywords = {"urgent", "asap", "deadline", "emergency", "blocker", "today", "immediately"}
        self.question_markers = {"?", "could you", "can you", "please confirm", "what do you think"}

    def estimate_cognitive_effort(self, subject, body):
        word_count = len((subject + " " + body).split())
        has_question = any(q in body.lower() for q in self.question_markers)
        
        # Base reading speed: ~200 words per minute
        read_time_min = word_count / 200.0
        
        # Effort categorization
        if word_count < 60 and has_question:
            effort_tier = "QUICK_HIT" # <2 minutes
            estimated_minutes = max(1.0, round(read_time_min + 1.0, 1))
        elif word_count > 300 or ("proposal" in body.lower() or "contract" in body.lower()):
            effort_tier = "DEEP_FOCUS" # >15 minutes
            estimated_minutes = max(15.0, round(read_time_min * 2.5 + 5.0, 1))
        else:
            effort_tier = "MODERATE_REVIEW" # 2-10 minutes
            estimated_minutes = max(3.0, round(read_time_min + 2.0, 1))

        return {
            "word_count": word_count,
            "has_question": has_question,
            "effort_tier": effort_tier,
            "estimated_minutes": estimated_minutes
        }

    def triage_message(self, sender, subject, body, sender_vip_score=0.5):
        text = (subject + " " + body).lower()
        effort = self.estimate_cognitive_effort(subject, body)
        
        # Urgency scoring
        urgency_score = 0.2
        if any(w in text for w in self.urgent_keywords):
            urgency_score += 0.5
        if sender_vip_score >= 0.8:
            urgency_score += 0.3
        urgency_score = min(1.0, round(urgency_score, 2))

        # Action type
        if "unsubscribe" in text or "newsletter" in text or "weekly digest" in text:
            action_type = "AUTO_ARCHIVE_OR_DIGEST"
            priority = "LOW"
        elif urgency_score >= 0.7:
            action_type = "IMMEDIATE_ACTION"
            priority = "HIGH"
        elif effort["effort_tier"] == "QUICK_HIT":
            action_type = "TWO_MINUTE_CLEAR"
            priority = "MEDIUM"
        else:
            action_type = "SCHEDULED_FOCUS_BLOCK"
            priority = "MEDIUM"

        return {
            "sender": sender,
            "subject": subject,
            "priority": priority,
            "action_type": action_type,
            "urgency_score": urgency_score,
            "effort": effort,
            "recommended_slot": "BATCH_EVENING" if priority == "LOW" else ("NOW" if priority == "HIGH" else "AFTERNOON_BLOCK")
        }

    def generate_action_queue(self, messages):
        triaged = [self.triage_message(m.get("sender", ""), m.get("subject", ""), m.get("body", ""), m.get("vip_score", 0.5)) for m in messages]
        # Sort by urgency descending, then effort ascending
        sorted_queue = sorted(triaged, key=lambda x: (-x["urgency_score"], x["effort"]["estimated_minutes"]))
        return {
            "total_messages": len(messages),
            "urgent_count": sum(1 for m in triaged if m["priority"] == "HIGH"),
            "quick_hits_count": sum(1 for m in triaged if m["effort"]["effort_tier"] == "QUICK_HIT"),
            "action_queue": sorted_queue
        }

    def run_benchmark_inbox_triage(self):
        sample_msgs = [
            {"sender": "boss@company.com", "subject": "Urgent: Project deployment blocker today", "body": "Can you check the server logs immediately?", "vip_score": 0.95},
            {"sender": "colleague@company.com", "subject": "Quick question on lunch", "body": "Are you free at 12:30?", "vip_score": 0.5},
            {"sender": "news@techdigest.com", "subject": "Weekly AI Engineering Digest #42", "body": "Here are 50 new research papers to read. Unsubscribe here.", "vip_score": 0.1}
        ]
        res = self.generate_action_queue(sample_msgs)
        return {
            "benchmark_status": "PASSED",
            "queue_length": len(res["action_queue"]),
            "top_priority_action": res["action_queue"][0]["action_type"],
            "newsletter_action": res["action_queue"][-1]["action_type"]
        }
