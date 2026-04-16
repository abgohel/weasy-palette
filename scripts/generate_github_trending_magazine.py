from __future__ import annotations

import argparse
import json
import re
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML


ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = ROOT / "src" / "weasyprint_flexoki" / "templates"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/135.0 Safari/537.36"
)


@dataclass
class RepoCard:
    rank: int
    owner: str
    repo: str
    category: str
    headline: str
    description: str
    stars: str
    trend: str
    language: str
    note: str
    url: str
    source_period: str


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate the GitHub trending magazine HTML and optional PDF export."
    )
    parser.add_argument(
        "--period",
        choices=["day", "week", "daily", "weekly"],
        default="week",
        help="Trending window to use for the main issue.",
    )
    parser.add_argument("--count", type=int, default=12, help="How many repos to include.")
    parser.add_argument(
        "--screen-output",
        default="examples/github-trending-magazine.html",
        help="Path for the interactive screen-first HTML output.",
    )
    parser.add_argument(
        "--print-output",
        default="examples/github-trending-magazine-print.html",
        help="Path for the print/export HTML output.",
    )
    parser.add_argument(
        "--pdf-output",
        default="dist/github-trending-magazine-weekly.pdf",
        help="Optional PDF output path. Pass an empty string to skip PDF generation.",
    )
    parser.add_argument(
        "--data-output",
        default="examples/github-trending-magazine-data.json",
        help="Optional JSON snapshot path for the generated issue data.",
    )
    return parser


def normalize_period(value: str) -> str:
    if value in {"day", "daily"}:
        return "daily"
    if value in {"week", "weekly"}:
        return "weekly"
    raise ValueError(f"Unsupported period: {value}")


def fetch_html(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request) as response:
        return response.read().decode("utf-8", errors="ignore")


def parse_trending_page(period: str) -> list[dict[str, str]]:
    url = f"https://github.com/trending?since={period}"
    soup = BeautifulSoup(fetch_html(url), "html.parser")
    articles = soup.select("article.Box-row")
    repos: list[dict[str, str]] = []
    for article in articles:
        link = article.select_one("h2 a")
        if link is None:
            continue

        href = (link.get("href") or "").strip("/")
        if not href or "/" not in href:
            continue
        owner, repo = href.split("/", 1)

        description_node = article.select_one("p")
        language_node = article.select_one('[itemprop="programmingLanguage"]')
        stars_node = article.select_one('a[href$="/stargazers"]')
        trend_match = re.search(r"([\d,]+)\s+stars\s+(today|this week)", article.get_text(" ", strip=True))

        repos.append(
            {
                "owner": owner.strip(),
                "repo": repo.strip(),
                "description": (
                    description_node.get_text(" ", strip=True)
                    if description_node is not None
                    else "No description provided."
                ),
                "language": (
                    language_node.get_text(" ", strip=True)
                    if language_node is not None
                    else "General"
                ),
                "stars": (
                    stars_node.get_text(" ", strip=True)
                    if stars_node is not None
                    else "0"
                ),
                "trend": trend_match.group(0) if trend_match else f"Trending {period}",
                "url": f"https://github.com/{owner.strip()}/{repo.strip()}",
                "source_period": period,
            }
        )
    return repos


CATEGORY_RULES: list[tuple[str, str]] = [
    ("memory", "Memory systems"),
    ("context", "Memory systems"),
    ("markdown", "Document pipeline"),
    ("document", "Document pipeline"),
    ("pdf", "Document pipeline"),
    ("agent", "Agent tooling"),
    ("claude", "Agent tooling"),
    ("codex", "Agent tooling"),
    ("skill", "Agent tooling"),
    ("workflow", "Agent tooling"),
    ("tutor", "Learning stack"),
    ("learn", "Learning stack"),
    ("notebook", "Learning stack"),
    ("course", "Learning stack"),
    ("finance", "Market models"),
    ("market", "Market models"),
    ("hedge", "Market models"),
    ("voice", "Voice tooling"),
    ("audio", "Voice tooling"),
    ("speech", "Voice tooling"),
    ("3d", "Spatial tools"),
    ("editor", "Spatial tools"),
    ("cloud", "Agent infrastructure"),
    ("deploy", "Agent infrastructure"),
    ("template", "Agent infrastructure"),
    ("file", "File intelligence"),
    ("archive", "Knowledge archive"),
    ("textbook", "Knowledge archive"),
    ("api", "Sourcebook"),
]


REPO_OVERRIDES: dict[str, dict[str, str]] = {
    "forrestchang/andrej-karpathy-skills": {
        "category": "Agent discipline",
        "headline": "The hottest repo is a reminder that prompting is still product design.",
        "note": "For your work, treat this as raw operating method, not scripture. Lift the parts that sharpen agent discipline, review loops, and memory hygiene, then fold those patterns into Axon instead of copying the whole aesthetic.",
    },
    "thedotmack/claude-mem": {
        "category": "Memory systems",
        "headline": "Memory layers are becoming the product, not just a feature bolted onto agents.",
        "note": "This maps directly onto Axon. Focus on retrieval timing, compression strategy, and what deserves to persist, but keep your own standard higher around signal quality and privacy boundaries.",
    },
    "microsoft/markitdown": {
        "category": "Document pipeline",
        "headline": "The mundane document layer is where a lot of useful AI work actually lands.",
        "note": "This is practical leverage for your real workflow. Keep it in mind whenever notes, office files, or reports need to become Markdown before they can feed search, summarization, or clean publication pipelines.",
    },
    "virattt/ai-hedge-fund": {
        "category": "Multi-agent finance",
        "headline": "Finance demos keep doubling as orchestration labs wearing a market wrapper.",
        "note": "Ignore the hedge-fund packaging if needed. The useful part is the role split, decision checkpoints, and evaluation structure, which are all portable to research, review, and agent collaboration work.",
    },
    "pascalorg/editor": {
        "category": "Spatial tools",
        "headline": "A 3D editor trends because interface can still beat abstraction.",
        "note": "Even if you never use it directly, this is worth reading as interface inspiration. Dense information sometimes gets easier when people manipulate space instead of scrolling through flat panes and lists.",
    },
    "google/magika": {
        "category": "File intelligence",
        "headline": "Boring infrastructure becomes interesting again when it quietly removes friction everywhere.",
        "note": "This is the kind of background reliability layer that pays off across mixed-document workflows. Keep it close for any pipeline that touches uploads, archives, or clinical files where quick type certainty prevents dumb downstream mistakes.",
    },
}


CATEGORY_HEADLINES = {
    "Agent discipline": "Process is becoming the differentiator, not just the model underneath it.",
    "Agent tooling": "Trending agent repos are really arguments about how work should be structured.",
    "Memory systems": "The memory layer is turning into the real product surface for agents.",
    "Document pipeline": "The boring document layer keeps winning because real work still runs through files.",
    "Learning stack": "Hands-on learning repos keep winning because they turn confusion into sequence.",
    "Market models": "Market-themed repos often double as orchestration experiments in disguise.",
    "Multi-agent finance": "Agent collectives keep borrowing firm metaphors because the coordination pattern works.",
    "Voice tooling": "Voice is becoming another editable medium, not just an output channel.",
    "Spatial tools": "Interface still matters, especially when complexity needs room to breathe.",
    "Agent infrastructure": "The platform fight is moving from chat wrappers to durable execution substrates.",
    "File intelligence": "Reliability tools get compelling fast when they quietly remove friction everywhere.",
    "Knowledge archive": "Archives trend when access itself becomes the product.",
    "Sourcebook": "Builder sourcebooks keep winning because leverage matters more than theatre.",
    "Engineering history": "Constraint and clarity still read as modern when the code is this honest.",
    "General": "The pattern under the repo matters more than the hype around it.",
}


CATEGORY_NOTES = {
    "Agent discipline": "For your work, mine this for reusable operating rules. The value is not in mirroring the repo voice, but in extracting methods that improve agent behavior, review quality, and failure recovery.",
    "Agent tooling": "Treat this as workflow inspiration. Ask whether it improves repeatability, sharper task boundaries, or better handoffs, then borrow only the pieces that hold up under real use.",
    "Memory systems": "Read this through the lens of Axon. Focus on compression, retrieval timing, and memory selection, because that is where continuity becomes genuinely useful instead of noisy.",
    "Document pipeline": "This is practical infrastructure for your actual work. Anything that makes messy files easier to convert, search, clean, and republish can pay off across briefs, handouts, and research notes.",
    "Learning stack": "Do not treat this as homework. Use it as a selective curriculum and pull the sections that sharpen your judgment about models, evaluation, and real-world failure modes.",
    "Market models": "You do not need the finance wrapper. The value is in the orchestration pattern, the evaluation loop, and the way specialized components are forced to justify decisions.",
    "Multi-agent finance": "Look past the branding and study the coordination pattern. Multi-role systems are useful when the task has real structure and benefits from explicit perspectives.",
    "Voice tooling": "This is relevant if you want more expressive outputs, patient-friendly audio summaries, or narrative delivery that feels designed instead of merely generated.",
    "Spatial tools": "Use this as interface inspiration. When information gets dense, spatial navigation can beat another layer of tabs, menus, and nested lists.",
    "Agent infrastructure": "Read this as substrate design. If you want agent work to become durable product behavior, the important questions are execution boundaries, session control, and how tools are wired.",
    "File intelligence": "Keep this in mind for any workflow touching mixed documents, uploads, or archives. Small reliability layers like this prevent downstream mistakes that are otherwise annoyingly expensive.",
    "Knowledge archive": "The real lesson here is packaging and access. Ask what makes a collection easy to adopt, explore, and reuse rather than just large.",
    "Sourcebook": "Use this when a project is bottlenecked by external data or services. It is more useful as a fast shortlist than as something to browse casually.",
    "Engineering history": "Treat this as a reset on elegance under pressure. Repos like this are useful when you want to remember what clean constraint feels like.",
    "General": "Ask what reusable system pattern sits under the surface, then decide whether it belongs anywhere in your own stack.",
}


def classify_repo(owner: str, repo: str, description: str, language: str) -> str:
    key = f"{owner}/{repo}".lower()
    if key == "chrislgarry/apollo-11":
        return "Engineering history"

    haystack = " ".join([owner, repo, description, language]).lower()
    for keyword, category in CATEGORY_RULES:
        if keyword in haystack:
            return category
    return "General"


def headline_for_repo(owner: str, repo: str, category: str) -> str:
    key = f"{owner}/{repo}".lower()
    if key in REPO_OVERRIDES and REPO_OVERRIDES[key].get("headline"):
        return REPO_OVERRIDES[key]["headline"]
    return CATEGORY_HEADLINES.get(category, CATEGORY_HEADLINES["General"])


def note_for_repo(owner: str, repo: str, category: str) -> str:
    key = f"{owner}/{repo}".lower()
    if key in REPO_OVERRIDES and REPO_OVERRIDES[key].get("note"):
        return REPO_OVERRIDES[key]["note"]
    return CATEGORY_NOTES.get(category, CATEGORY_NOTES["General"])


def category_for_repo(owner: str, repo: str, description: str, language: str) -> str:
    key = f"{owner}/{repo}".lower()
    if key in REPO_OVERRIDES and REPO_OVERRIDES[key].get("category"):
        return REPO_OVERRIDES[key]["category"]
    return classify_repo(owner, repo, description, language)


def build_repo_cards(items: Iterable[dict[str, str]]) -> list[RepoCard]:
    cards: list[RepoCard] = []
    for rank, item in enumerate(items, start=1):
        category = category_for_repo(
            item["owner"], item["repo"], item["description"], item["language"]
        )
        cards.append(
            RepoCard(
                rank=rank,
                owner=item["owner"],
                repo=item["repo"],
                category=category,
                headline=headline_for_repo(item["owner"], item["repo"], category),
                description=item["description"],
                stars=item["stars"],
                trend=item["trend"],
                language=item["language"],
                note=note_for_repo(item["owner"], item["repo"], category),
                url=item["url"],
                source_period=item["source_period"],
            )
        )
    return cards


def collect_trending_repos(period: str, count: int) -> tuple[list[RepoCard], str | None]:
    primary = parse_trending_page(period)
    combined: list[dict[str, str]] = []
    seen: set[str] = set()

    def add_items(items: Iterable[dict[str, str]]) -> None:
        for item in items:
            key = f"{item['owner']}/{item['repo']}".lower()
            if key in seen:
                continue
            seen.add(key)
            combined.append(item)
            if len(combined) >= count:
                return

    add_items(primary)
    note = None
    if len(combined) < count and period == "weekly":
        before = len(combined)
        add_items(parse_trending_page("daily"))
        topped_up = len(combined) - before
        if topped_up > 0:
            note = (
                f"GitHub returned {before} weekly repos, so this issue tops up the final "
                f"{topped_up} slot{'s' if topped_up != 1 else ''} with current daily picks "
                "to preserve the 14-page format."
            )

    if len(combined) < count:
        raise RuntimeError(
            f"Could only collect {len(combined)} trending repos for a {count}-repo issue."
        )

    return build_repo_cards(combined[:count]), note


def build_context(period: str, repos: list[RepoCard], issue_note: str | None) -> dict[str, object]:
    now = datetime.now(timezone.utc)
    issue_label = "DAY" if period == "daily" else "WEEK"
    return {
        "issue_label": issue_label,
        "issue_date": now.strftime("%d %b %Y"),
        "generated_at": now.strftime("%d %b %Y %H:%M UTC"),
        "total_pages": len(repos) + 2,
        "repos": repos,
        "issue_note": issue_note,
    }


def render_templates(context: dict[str, object], screen_output: Path, print_output: Path) -> None:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=select_autoescape(enabled_extensions=("html", "xml")),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    screen_template = env.get_template("github-trending-magazine-screen.html.j2")
    print_template = env.get_template("github-trending-magazine-print.html.j2")

    screen_output.parent.mkdir(parents=True, exist_ok=True)
    print_output.parent.mkdir(parents=True, exist_ok=True)
    screen_output.write_text(screen_template.render(**context), encoding="utf-8")
    print_output.write_text(print_template.render(**context), encoding="utf-8")


def write_data_snapshot(data_output: Path, context: dict[str, object]) -> None:
    data_output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "issue_label": context["issue_label"],
        "issue_date": context["issue_date"],
        "generated_at": context["generated_at"],
        "total_pages": context["total_pages"],
        "issue_note": context["issue_note"],
        "repos": [asdict(repo) for repo in context["repos"]],
    }
    data_output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def render_pdf(print_output: Path, pdf_output: Path) -> None:
    pdf_output.parent.mkdir(parents=True, exist_ok=True)
    HTML(filename=str(print_output), base_url=str(print_output.parent)).write_pdf(str(pdf_output))


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    period = normalize_period(args.period)
    screen_output = (ROOT / args.screen_output).resolve()
    print_output = (ROOT / args.print_output).resolve()
    pdf_output = (ROOT / args.pdf_output).resolve() if args.pdf_output else None
    data_output = (ROOT / args.data_output).resolve() if args.data_output else None

    repos, issue_note = collect_trending_repos(period=period, count=args.count)
    context = build_context(period=period, repos=repos, issue_note=issue_note)
    render_templates(context=context, screen_output=screen_output, print_output=print_output)
    if data_output is not None:
        write_data_snapshot(data_output=data_output, context=context)
    if pdf_output is not None:
        render_pdf(print_output=print_output, pdf_output=pdf_output)

    print(f"Generated {screen_output}")
    print(f"Generated {print_output}")
    if data_output is not None:
        print(f"Generated {data_output}")
    if pdf_output is not None:
        print(f"Generated {pdf_output}")


if __name__ == "__main__":
    main()
