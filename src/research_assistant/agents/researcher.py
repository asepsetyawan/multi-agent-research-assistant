from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from research_assistant.config import get_settings
from research_assistant.tools.search import search_web


RESEARCHER_PROMPT = ChatPromptTemplate.from_messages(
  [
    (
      "system",
      "You are a research analyst. Use the provided web search snippets to answer the sub-question. "
      "Be factual, concise, and cite sources inline as [source title]. "
      "If evidence is weak, say what is missing.",
    ),
    (
      "human",
      "Main question: {question}\n"
      "Sub-question: {subtask}\n\n"
      "Search results:\n{search_results}",
    ),
  ]
)


def research_subtask(question: str, subtask: str) -> dict:
  settings = get_settings()
  snippets = search_web(subtask)
  formatted_results = "\n\n".join(
    f"- {item['title']} ({item['url']})\n  {item['content']}" for item in snippets
  )

  llm = ChatOpenAI(model=settings.openai_model, temperature=0.2)
  chain = RESEARCHER_PROMPT | llm
  summary = chain.invoke(
    {
      "question": question,
      "subtask": subtask,
      "search_results": formatted_results,
    }
  )

  return {
    "subtask": subtask,
    "summary": summary.content,
    "sources": snippets,
  }
