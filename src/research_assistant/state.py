import operator
from typing import Annotated, TypedDict


class ResearchState(TypedDict):
  """Shared state flowing through the LangGraph workflow."""

  question: str
  subtasks: list[str]
  research_results: Annotated[list[dict], operator.add]
  critique: str
  gaps: list[str]
  needs_more_research: bool
  report: str
  iteration: int
  max_iterations: int


class ResearcherState(TypedDict):
  """Per-subtask state for parallel researcher nodes."""

  subtask: str
  question: str
