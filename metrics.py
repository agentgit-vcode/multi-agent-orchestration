"""
Metrics tracking for LLM calls and agent execution.
Stores token usage, timing, and model information for analytics.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from datetime import datetime
import threading


@dataclass
class LLMCallMetrics:
    """Metrics for a single LLM API call."""
    agent_name: str
    provider: str            # 'google' or 'openai'
    model: str               # e.g. 'gemini-pro-latest', 'gpt-3.5-turbo'
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    duration_seconds: float = 0.0
    tokens_estimated: bool = False  # True for Gemini (no exact counts)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class TaskMetrics:
    """Aggregated metrics for a complete task run."""
    task_id: str
    question: str = ''
    model: str = ''
    provider: str = ''
    agent_calls: List[LLMCallMetrics] = field(default_factory=list)
    agent_timings: Dict[str, float] = field(default_factory=dict)  # agent_name -> seconds
    total_duration_seconds: float = 0.0
    total_tokens: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def add_call(self, metrics: LLMCallMetrics):
        self.agent_calls.append(metrics)
        self.total_tokens += metrics.total_tokens

    def to_dict(self) -> dict:
        return {
            'task_id': self.task_id,
            'question': self.question[:100] + ('...' if len(self.question) > 100 else ''),
            'model': self.model,
            'provider': self.provider,
            'agent_calls': [c.to_dict() for c in self.agent_calls],
            'agent_timings': self.agent_timings,
            'total_duration_seconds': round(self.total_duration_seconds, 2),
            'total_tokens': self.total_tokens,
            'timestamp': self.timestamp,
        }


class MetricsStore:
    """Thread-safe in-memory store for task metrics."""

    def __init__(self, max_history: int = 50):
        self._history: List[TaskMetrics] = []
        self._lock = threading.Lock()
        self._max_history = max_history

    def record(self, task_metrics: TaskMetrics):
        """Store completed task metrics."""
        with self._lock:
            self._history.append(task_metrics)
            # Trim to max
            if len(self._history) > self._max_history:
                self._history = self._history[-self._max_history:]

    def get_task_metrics(self, task_id: str) -> Optional[TaskMetrics]:
        """Get metrics for a specific task."""
        with self._lock:
            for m in reversed(self._history):
                if m.task_id == task_id:
                    return m
        return None

    def get_history(self) -> List[dict]:
        """Get all task metrics as dicts (most recent first)."""
        with self._lock:
            return [m.to_dict() for m in reversed(self._history)]

    def get_aggregate_stats(self) -> dict:
        """Get aggregate statistics across all tracked tasks."""
        with self._lock:
            if not self._history:
                return {
                    'total_tasks': 0,
                    'total_tokens': 0,
                    'avg_tokens_per_task': 0,
                    'avg_duration_seconds': 0,
                    'models_used': {},
                }

            total_tasks = len(self._history)
            total_tokens = sum(m.total_tokens for m in self._history)
            total_duration = sum(m.total_duration_seconds for m in self._history)

            # Count model usage
            models_used: Dict[str, int] = {}
            for m in self._history:
                key = f"{m.provider}/{m.model}"
                models_used[key] = models_used.get(key, 0) + 1

            return {
                'total_tasks': total_tasks,
                'total_tokens': total_tokens,
                'avg_tokens_per_task': round(total_tokens / total_tasks),
                'avg_duration_seconds': round(total_duration / total_tasks, 2),
                'models_used': models_used,
            }


# Global metrics store
metrics_store = MetricsStore()
