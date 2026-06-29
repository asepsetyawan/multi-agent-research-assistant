from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from research_assistant.config import get_settings


class CritiqueOutput(BaseModel):
  is_sufficient: bool = Field(description="Whether research is enough to write a solid report.")
  critique: str = Field(description="What is strong, weak, or missing in the gathered research.")
  gaps: list[str] = Field(description="Specific gaps that need another research pass.")


CRITIC_PROMPT = ChatPromptTemplate.from_messages(
  [
    (
      "system",
      "You are a skeptical research critic. Evaluate whether collected notes are enough "
      "to answer the main question with nuance and evidence. Identify concrete gaps.",
    ),
    (
      "human",
      "Main question: {question}\n\nResearch notes:\n{notes}",
    ),
  ]
)


def create_critic():
  settings = get_settings()
  llm = ChatOpenAI(model=settings.openai_model, temperature=0.1)
  return CRITIC_PROMPT | llm.with_structured_output(CritiqueOutput)


def critique_research(question: str, research_results: list[dict]) -> CritiqueOutput:
  notes = "\n\n".join(
    f"### {item['subtask']}\n{item['summary']}" for item in research_results
  )
  critic = create_critic()
  return critic.invoke({"question": question, "notes": notes or "No research yet."})
