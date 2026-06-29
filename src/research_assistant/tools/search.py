from research_assistant.config import get_settings


def _mock_search(query: str) -> list[dict]:
  return [
    {
      "title": f"Overview: {query}",
      "url": "https://example.com/overview",
      "content": (
        f"Mock result for '{query}'. LangGraph enables stateful multi-agent workflows "
        "with checkpointing, interrupts, and parallel node execution."
      ),
    },
    {
      "title": f"Recent developments on {query}",
      "url": "https://example.com/recent",
      "content": (
        "Teams use planner-researcher-critic-writer patterns to improve answer quality "
        "and reduce hallucinations via grounded web search."
      ),
    },
  ]


def search_web(query: str, max_results: int = 4) -> list[dict]:
  settings = get_settings()

  if settings.tavily_api_key:
    from langchain_community.tools.tavily_search import TavilySearchResults

    tool = TavilySearchResults(
      max_results=max_results,
      tavily_api_key=settings.tavily_api_key,
    )
    raw_results = tool.invoke({"query": query})
    return [
      {
        "title": item.get("title", "Untitled"),
        "url": item.get("url", ""),
        "content": item.get("content", item.get("snippet", "")),
      }
      for item in raw_results
    ]

  return _mock_search(query)
