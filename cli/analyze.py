# cli/analyze.py
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

import click

@click.command()
@click.argument("pdf_path", type=click.Path(exists=True))
def analyze(pdf_path):
    """Extract and analyze a Supreme Court judgment PDF."""

    pdf = Path(pdf_path)
    click.echo(f"\n⚖️  Judgment Reasoning Analyzer")
    click.echo("─" * 40)

    try:
        click.echo("[1/4] Extracting text from PDF...")
        from ingestion.pdf_extractor import extract_text
        extract_text(pdf)
        click.secho("      ✓ Done", fg="green")

        click.echo("[2/4] Detecting sections...")
        from ingestion.section_detector import detect_sections
        found = detect_sections()
        click.secho(f"      ✓ Found {len(found)} sections", fg="green")

        click.echo("[3/4] Splitting and storing paragraphs...")
        from ingestion.paragraph_splitter import split_paragraphs
        from ingestion.paragraph_store import store_paragraphs
        split_paragraphs()
        store_paragraphs()
        click.secho("      ✓ Done", fg="green")

        click.echo("[4/4] Extracting legal entities...")
        from ingestion.metadata_extractor import extract_metadata
        from ingestion.citation_extractor import extract_citations
        from ingestion.precedent_extractor import extract_precedents
        extract_metadata()
        extract_citations()
        extract_precedents()
        click.secho("      ✓ Done", fg="green")

        click.echo("\n─" * 40)
        click.secho("✅  Analysis complete.\n", fg="green", bold=True)

        # Print summary
        import json
        INGESTION_DIR = BASE_DIR / "ingestion"

        meta = json.loads((INGESTION_DIR / "metadata.json").read_text(encoding="utf-8"))
        click.secho("Case:   ", fg="cyan", nl=False)
        click.echo(meta.get("case_name", "—"))
        click.secho("Date:   ", fg="cyan", nl=False)
        click.echo(meta.get("date", "—"))

        citations = json.loads((INGESTION_DIR / "citations.json").read_text(encoding="utf-8"))
        click.secho("Acts:   ", fg="cyan", nl=False)
        click.echo(", ".join(citations.get("articles", [])))

        precedents = json.loads((INGESTION_DIR / "precedents.json").read_text(encoding="utf-8"))
        count = len(precedents.get("extracted_citations", []))
        click.secho("Cases cited: ", fg="cyan", nl=False)
        click.echo(str(count))

        click.echo("\nRun `judgment show` to see full output.")
        click.echo("Run `judgment query \"your question\"` to query the judgment.")

    except Exception as e:
        click.secho(f"\n✗ Error: {e}", fg="red", bold=True)
        sys.exit(1)