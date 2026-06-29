from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from research_assistant.config import get_settings


WRITER_PROMPT = ChatPromptTemplate.from_messages(
  [
    (
      "system",
      "You are a technical writer. Synthesize research notes into a clear, well-structured report "
      "with an executive summary, key findings, trade-offs, and a numbered reference list. "
      "Use markdown headings. Cite sources from the notes.",
    ),
    (
      "human",
      "Question: {question}\n\nResearch notes:\n{notes}\n\nCritique context:\n{critique}",
    ),
  ]
)


def write_report(question: str, research_results: list[dict], critique: str = "") -> str:
  settings = get_settings()
  notes = "\n\n".join(
    f"### {item['subtask']}\n{item['summary']}\n"
    f"Sources: {', '.join(source['title'] for source in item.get('sources', []))}"
    for item in research_results
  )

  llm = ChatOpenAI(model=settings.openai_model, temperature=0.3)
  chain = WRITER_PROMPT | llm
  result = chain.invoke(
    {
      "question": question,
      "notes": notes,
      "critique": critique or "No critique provided.",
    }
  )
  return result.content
