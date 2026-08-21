import logging
from typing import Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class ModelContextProtocol:
    """Model Context Protocol - Manages context and memory for agents"""
    
    def __init__(self):
        self.context_stack = []
        self.memory_store = {}
        self.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        logger.info(f"MCP initialized - Session: {self.session_id}")
    
    def push_context(self, context_type: str, data: Dict) -> None:
        """Push new context to stack"""
        context = {
            'type': context_type,
            'data': data,
            'timestamp': datetime.now().isoformat(),
            'agent_id': data.get('agent_id', 'unknown')
        }
        self.context_stack.append(context)
        logger.info(f"Context pushed: {context_type}")
    
    def pop_context(self) -> Dict:
        """Pop context from stack"""
        if self.context_stack:
            context = self.context_stack.pop()
            logger.info(f"Context popped: {context['type']}")
            return context
        return None
    
    def get_current_context(self) -> Dict:
        """Get current context"""
        if self.context_stack:
            return self.context_stack[-1]
        return None
    
    def save_to_memory(self, key: str, value: Any) -> None:
        """Save data to memory"""
        self.memory_store[key] = {
            'value': value,
            'timestamp': datetime.now().isoformat()
        }
        logger.info(f"Saved to memory: {key}")
    
    def get_from_memory(self, key: str) -> Any:
        """Get data from memory"""
        if key in self.memory_store:
            return self.memory_store[key]['value']
        return None
    
    def clear_memory(self) -> None:
        """Clear all memory"""
        self.memory_store.clear()
        logger.info("Memory cleared")
    
    def get_session_summary(self) -> Dict:
        """Get session summary"""
        return {
            'session_id': self.session_id,
            'context_count': len(self.context_stack),
            'memory_items': len(self.memory_store),
            'timestamp': datetime.now().isoformat()
        }