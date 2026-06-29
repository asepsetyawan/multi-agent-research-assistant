import argparse
import sys

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from research_assistant.graph.workflow import run_research


def main() -> None:
  parser = argparse.ArgumentParser(description="Run the multi-agent research assistant.")
  parser.add_argument("question", help="Research question to investigate.")
  args = parser.parse_args()

  console = Console()
  console.print(Panel.fit(args.question, title="Research Question", border_style="cyan"))

  try:
    result = run_research(args.question)
  except Exception as exc:
    console.print(f"[red]Research failed:[/red] {exc}")
    sys.exit(1)

  console.print("\n[bold green]Subtasks[/bold green]")
  for subtask in result["subtasks"]:
    console.print(f"- {subtask}")

  console.print("\n[bold green]Critique[/bold green]")
  console.print(result.get("critique", "No critique generated."))

  console.print("\n[bold green]Final Report[/bold green]")
  console.print(Markdown(result.get("report", "No report generated.")))


if __name__ == "__main__":
  main()
