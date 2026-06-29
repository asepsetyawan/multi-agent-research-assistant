from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from research_assistant.config import get_settings


class PlanOutput(BaseModel):
  subtasks: list[str] = Field(
    description="Focused research sub-questions that together answer the main question."
  )


PLANNER_PROMPT = ChatPromptTemplate.from_messages(
  [
    (
      "system",
      "You are a research planner. Break complex questions into concrete, searchable sub-questions. "
      "Each subtask should target one angle (definitions, recent developments, trade-offs, examples). "
      "Avoid overlap. Return only the requested structured output.",
    ),
    (
      "human",
      "Main question: {question}\n\n"
      "Create up to {max_subtasks} sub-questions. "
      "If gaps from a prior critique are provided, prioritize covering those gaps.\n"
      "Prior critique: {critique}\n"
      "Gaps to address: {gaps}",
    ),
  ]
)


def create_planner():
  settings = get_settings()
  llm = ChatOpenAI(model=settings.openai_model, temperature=0.2)
  return PLANNER_PROMPT | llm.with_structured_output(PlanOutput)


def plan_research(question: str, critique: str = "", gaps: list[str] = []) -> list[str]:
  planner = create_planner()
  settings = get_settings()
  result = planner.invoke(
    {
      "question": question,
      "critique": critique or "None",
      "gaps": ", ".join(gaps) if gaps else "None",
      "max_subtasks": settings.max_subtasks,
    }
  )
  return result.subtasks[:settings.max_subtasks]
