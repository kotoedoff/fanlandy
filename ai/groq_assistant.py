from groq import Groq
from database.sessions import get_findings, get_chat_history
import json

SYSTEM_PROMPT = """OSINT assistant. Analyze findings, suggest tools/steps, identify patterns. Professional, concise, legal only."""

class GroqAssistant:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        
    def get_context(self, session_id, session_data):
        findings = get_findings(session_id)
        if not findings:
            return f"Target: {session_data[2] or 'Not set'}"
        context = f"Target: {session_data[2] or 'Not set'}\nFindings:\n"
        for tool, data, timestamp in findings[-5:]:
            context += f"{tool}: {data[:100]}...\n"
        return context
    
    def chat(self, session_id, session_data, user_message):
        history = get_chat_history(session_id)
        context = self.get_context(session_id, session_data)
        
        messages = [{"role": "system", "content": f"{SYSTEM_PROMPT}\n{context}"}]
        
        for role, content in history[-10:]:
            messages.append({"role": role, "content": content})
        
        messages.append({"role": "user", "content": user_message})
        
        completion = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_completion_tokens=2048,
            stream=True,
            stop=None
        )
        
        full_response = ""
        for chunk in completion:
            content = chunk.choices[0].delta.content or ""
            full_response += content
            yield content
        
        return full_response
