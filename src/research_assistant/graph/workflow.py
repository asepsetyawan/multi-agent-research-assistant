from langgraph.graph import END, START, StateGraph
from langgraph.types import Send

from research_assistant.agents.critic import critique_research
from research_assistant.agents.planner import plan_research
from research_assistant.agents.researcher import research_subtask
from research_assistant.agents.writer import write_report
from research_assistant.config import get_settings
from research_assistant.state import ResearchState, ResearcherState


def planner_node(state: ResearchState) -> dict:
  subtasks = plan_research(
    question=state["question"],
    critique=state.get("critique", ""),
    gaps=state.get("gaps", []),
  )
  return {"subtasks": subtasks}


def dispatch_researchers(state: ResearchState) -> list[Send]:
  return [
    Send(
      "researcher",
      {"subtask": subtask, "question": state["question"]},
    )
    for subtask in state["subtasks"]
  ]


def researcher_node(state: ResearcherState) -> dict:
  result = research_subtask(question=state["question"], subtask=state["subtask"])
  return {"research_results": [result]}


def critic_node(state: ResearchState) -> dict:
  critique = critique_research(state["question"], state["research_results"])
  iteration = state.get("iteration", 0) + 1
  needs_more = not critique.is_sufficient and iteration < state["max_iterations"]
  return {
    "critique": critique.critique,
    "gaps": critique.gaps,
    "needs_more_research": needs_more,
    "iteration": iteration,
  }


def writer_node(state: ResearchState) -> dict:
  report = write_report(
    question=state["question"],
    research_results=state["research_results"],
    critique=state.get("critique", ""),
  )
  return {"report": report}


def route_after_critic(state: ResearchState) -> str:
  if state.get("needs_more_research"):
    return "planner"
  return "writer"


def build_research_graph():
  graph = StateGraph(ResearchState)

  graph.add_node("planner", planner_node)
  graph.add_node("researcher", researcher_node)
  graph.add_node("critic", critic_node)
  graph.add_node("writer", writer_node)

  graph.add_edge(START, "planner")
  graph.add_conditional_edges("planner", dispatch_researchers, ["researcher"])
  graph.add_edge("researcher", "critic")
  graph.add_conditional_edges("critic", route_after_critic, {"planner": "planner", "writer": "writer"})
  graph.add_edge("writer", END)

  return graph.compile()


def run_research(question: str) -> ResearchState:
  settings = get_settings()
  app = build_research_graph()
  initial_state: ResearchState = {
    "question": question,
    "subtasks": [],
    "research_results": [],
    "critique": "",
    "gaps": [],
    "needs_more_research": False,
    "report": "",
    "iteration": 0,
    "max_iterations": settings.max_research_iterations,
  }
  return app.invoke(initial_state)
