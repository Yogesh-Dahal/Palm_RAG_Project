import os
import json
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=0,
    decode_responses=True
)

HISTORY_LIMIT = 10


def get_history(session_id: str) -> list[str]:
    """
    Returns last N messages as:
    ['user: ...', 'assistant: ...']
    """
    key = f"chat:{session_id}"
    raw_messages = r.lrange(key, 0, HISTORY_LIMIT - 1)

    messages = [json.loads(m) for m in reversed(raw_messages)]
    return [f"{m['role']}: {m['content']}" for m in messages]


def save_message(session_id: str, role: str, content: str):
    """
    Save a chat message into Redis.
    """
    key = f"chat:{session_id}"
    payload = json.dumps({
        "role": role,
        "content": content
    })

    r.lpush(key, payload)
    r.ltrim(key, 0, HISTORY_LIMIT - 1)
