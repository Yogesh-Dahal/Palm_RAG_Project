INTENT_PROMPT = """
You are an intent classifier.

User message:
{query}

Return STRICT JSON only.

If booking intent:
{{ "intent": "booking" }}

Else:
{{ "intent": "qa" }}
"""


RAG_PROMPT = """
You are an assistant answering questions using ONLY the context below.

Context:
{context}

Conversation history:
{history}

User question:
{query}

If the answer is not in the context, say you don't know.
"""


BOOKING_PROMPT = """
Extract interview booking details from the conversation.

Conversation history:
{history}

User message:
{query}

Return STRICT JSON:
{{
  "name": null or string,
  "email": null or string,
  "date": null or YYYY-MM-DD,
  "time": null or HH:MM
}}
"""
