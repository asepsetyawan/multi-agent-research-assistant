from unittest.mock import patch

from research_assistant.graph.workflow import build_research_graph


def test_graph_compiles():
  graph = build_research_graph()
  assert graph is not None


@patch("research_assistant.graph.workflow.plan_research", return_value=["What is LangGraph?"])
@patch(
  "research_assistant.graph.workflow.research_subtask",
  return_value={
    "subtask": "What is LangGraph?",
    "summary": "LangGraph is a graph orchestration framework.",
    "sources": [{"title": "LangGraph", "url": "https://example.com", "content": "..."}],
  },
)
@patch(
  "research_assistant.graph.workflow.critique_research",
  return_value=type(
    "Critique",
    (),
    {
      "is_sufficient": True,
      "critique": "Sufficient for a short overview.",
      "gaps": [],
    },
  )(),
)
@patch(
  "research_assistant.graph.workflow.write_report",
  return_value="# Report\nLangGraph helps orchestrate agents.",
)
def test_workflow_runs_with_mocks(*_mocks):
  graph = build_research_graph()
  result = graph.invoke(
    {
      "question": "What is LangGraph?",
      "subtasks": [],
      "research_results": [],
      "critique": "",
      "gaps": [],
      "needs_more_research": False,
      "report": "",
      "iteration": 0,
      "max_iterations": 2,
    }
  )
  assert "LangGraph" in result["report"]
