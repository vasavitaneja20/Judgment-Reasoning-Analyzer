# cli/show.py
import sys
import json
from pathlib import Path

BASE_DIR      = Path(__file__).parent.parent
INGESTION_DIR = BASE_DIR / "ingestion"
DATA_DIR      = BASE_DIR / "data"
sys.path.insert(0, str(BASE_DIR))

import click

def _load(path):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return None

@click.command()
@click.option("--section", default="all",
              type=click.Choice(["all","facts","submissions","analysis","conclusion"]),
              help="Which section to display")
def show(section):
    """Display the structured judgment output."""

    click.echo(f"\n⚖️  Judgment Output")
    click.echo("─" * 60)

    # Metadata
    meta = _load(INGESTION_DIR / "metadata.json")
    if meta:
        click.secho("CASE",    fg="cyan", bold=True)
        click.echo(f"  Name:   {meta.get('case_name','—')}")
        click.echo(f"  Date:   {meta.get('date','—')}")

    # Judgment sections
    judgment = _load(INGESTION_DIR / "structured_judgment.json")
    if judgment:
        sections_to_show = (
            ["facts","submissions","analysis","conclusion"]
            if section == "all" else [section]
        )
        for s in sections_to_show:
            click.echo(f"\n{'─'*60}")
            click.secho(s.upper(), fg="cyan", bold=True)
            text = judgment.get(s, "Not available")
            click.echo(text[:1500] + ("…" if len(text) > 1500 else ""))

    # Citations
    citations = _load(INGESTION_DIR / "citations.json")
    if citations:
        click.echo(f"\n{'─'*60}")
        click.secho("STATUTES CITED", fg="cyan", bold=True)
        click.echo("  Articles: " + ", ".join(citations.get("articles", [])))
        click.echo("  Sections: " + ", ".join(citations.get("sections", [])[:10]))

    # Precedents
    precedents = _load(INGESTION_DIR / "precedents.json")
    if precedents:
        cases = precedents.get("extracted_citations", [])
        click.echo(f"\n{'─'*60}")
        click.secho("PRECEDENTS CITED", fg="cyan", bold=True)
        for c in cases[:10]:
            click.echo(f"  · {c}")
        if len(cases) > 10:
            click.echo(f"  … and {len(cases)-10} more")

    click.echo(f"\n{'─'*60}\n")