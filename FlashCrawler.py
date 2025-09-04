#!/usr/bin/env python3

"""
FlashCrawler v2.0 – JS-Aware Web Crawler using Playwright with Option Random User-Agent
"""

import os
import re
import time
import asyncio
import random
import argparse
from pathlib import Path
from urllib.parse import urljoin, urlparse, parse_qs

from bs4 import BeautifulSoup
from rich import box
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

from playwright.async_api import async_playwright

# ────────────── CLI Configuration ────────────── #
console = Console()
parser = argparse.ArgumentParser(
    description="⚡ FlashCrawler – BFS Web Crawler v2.0.0",
    epilog="""
Examples:
  python FlashCrawler.py -u https://example.com
  python FlashCrawler.py -u https://example.com --save -t 3
GitHub: https://github.com/SKaif009, Author: BlackForgeX
""",
    formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument("-u", "--url", help="Target URL to crawl", required=True)
parser.add_argument("-d", "--depth", type=int, default=100, help="Max number of pages to crawl")
parser.add_argument("-t", "--time", type=int, default=1, help="Delay between requests in seconds")
parser.add_argument("-s", "--save", action="store_true", help="Save results to 'results/'")
parser.add_argument("--req-timeout", type=int, default=15, help="Request timeout in seconds")
parser.add_argument("--dedup-params", action="store_true", help="Deduplicate based on parameter signature")
parser.add_argument("-rua", "--random-agent", action="store_true", help="Use a random User-Agent from user_agents.txt")
args = parser.parse_args()

TIMEOUT = args.req_timeout * 1000
DELAY = args.time
MAX_PAGES = args.depth
SAVE_RESULTS = args.save
DEDUP_PARAM_SIG = args.dedup_params

visited = set()
queue = set([args.url])
found = set()
allowed_domain = urlparse(args.url).netloc
seen_param_signatures = set()
results_dir = Path("results")
results_dir.mkdir(exist_ok=True)

def get_random_user_agent():
    try:
        with open("user_agents.txt", "r") as f:
            agents = [line.strip() for line in f if line.strip()]
            return random.choice(agents)
    except FileNotFoundError:
        console.print("[red]✖ user_agents.txt not found. Using default User-Agent.[/]")
        return None

RANDOM_UA = get_random_user_agent() if args.random_agent else None

def is_valid(url: str) -> bool:
    p = urlparse(url)
    return p.scheme in {"http", "https"} and p.netloc == allowed_domain

def normalize_param_signature(url: str) -> str:
    parsed = urlparse(url)
    keys = sorted(parse_qs(parsed.query).keys())
    if keys:
        return f"{parsed.path}?params={'&'.join(keys)}"
    return parsed.path

def extract_links(soup, base_url):
    tags = soup.find_all(["a", "form", "script", "iframe"])
    links = set()
    for tag in tags:
        href = tag.get("href") or tag.get("action") or tag.get("src")
        if href:
            abs_url = urljoin(base_url, href)
            if is_valid(abs_url):
                if DEDUP_PARAM_SIG:
                    sig = normalize_param_signature(abs_url)
                    if sig in seen_param_signatures:
                        continue
                    seen_param_signatures.add(sig)
                links.add(abs_url)
    return links

def extract_endpoints_from_js(text):
    return set(re.findall(r'["\'](/[^"\\>\s]+)["\']', text))

async def extract(page, url):
    links = set()
    try:
        if RANDOM_UA:
            await page.set_extra_http_headers({"User-Agent": RANDOM_UA})
        await page.set_viewport_size({"width": 1366, "height": 768})
        await page.goto(url, wait_until="load", timeout=TIMEOUT)
        await asyncio.sleep(DELAY)
        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")
        links |= extract_links(soup, page.url)
        for script in soup.find_all("script"):
            if script.string:
                for ep in extract_endpoints_from_js(script.string):
                    abs_url = urljoin(page.url, ep)
                    if is_valid(abs_url):
                        links.add(abs_url)
    except Exception as e:
        console.log(f"[red]✖ Error on:[/] {url} – {e}")
    return links

async def crawl():
    banner()
    start = time.perf_counter()
    total = 0

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        with Progress(
            SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
            BarColumn(), TextColumn("[blue]{task.completed}/{task.total} pages"),
            TimeElapsedColumn(), console=console, transient=True,
        ) as prog:
            task = prog.add_task("Crawling", total=MAX_PAGES)
            while queue and total < MAX_PAGES:
                url = queue.pop()
                if url in visited:
                    continue
                visited.add(url)
                prog.update(task, advance=1, description=f"[green]Visiting[/] {urlparse(url).path or '/'}")
                links = await extract(page, url)
                found.update(links)
                for link in links:
                    if link not in visited and link not in queue:
                        queue.add(link)
                total += 1
        await browser.close()

    elapsed = time.perf_counter() - start
    console.print(f"\n[bold green]✔ Finished in {elapsed:.2f}s[/]")
    show_table()
    if SAVE_RESULTS:
        save_results()
def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print("[bold yellow] ⚡ [/] [bold bright_magenta] Flash Crawler v2.0 [/] [bold yellow] ⚡ [/]", justify="center")
    console.rule("[bold yellow] ⚡ [bold cyan] FlashCrawler – BFS Web Crawler [bold yellow] ⚡", style="bright_magenta")
    console.print(f"[bold cyan]🌐 Seed:[/] {args.url}    [bold cyan]⏱ Delay:[/] {DELAY}s    [bold cyan]⏰ Timeout:[/] {TIMEOUT/1000:.1f}s")
    if RANDOM_UA:
        console.print(f"[bold cyan]🕵 Random UA:[/] {RANDOM_UA[:60]}...\\n")
    else:
        console.print("[yellow]Tip:[/] Use [bold]--random-agent[/] to simulate real browser headers when a site blocks Playwright.\\n")


def show_table():
    table = Table(title="Discovered URLs", box=box.SIMPLE_HEAVY)
    table.add_column("#", style="cyan", width=4)
    table.add_column("URL", style="white")
    for i, url in enumerate(sorted(visited.union(found)), 1):
        table.add_row(str(i), url)
    console.print(table)
    console.rule("[bold yellow]⚡[bold cyan] FlashCrawler", style="bright_magenta")

def save_results():
    all_urls = visited.union(found)
    urls_file = results_dir / "found_urls.txt"
    params_file = results_dir / "found_parameters.txt"
    dedup_file = results_dir / "deduplicate_params.txt"

    with urls_file.open("w") as u, params_file.open("w") as p, dedup_file.open("w") as d:
        for url in sorted(all_urls):
            u.write(url + "\n")
            if '?' in url:
                p.write(url + "\n")
        if DEDUP_PARAM_SIG:
            for sig in sorted(seen_param_signatures):
                d.write(sig + "\n")

    console.print(f"[green]✔ Saved to:[/] {results_dir}")
    console.print(f"[cyan]Total URLs:[/] {len(all_urls)}")
    console.print(f"[cyan]With parameters:[/] {len([u for u in all_urls if '?' in u])}")
    if DEDUP_PARAM_SIG:
        console.print(f"[cyan]Unique param patterns:[/] {len(seen_param_signatures)}")

if __name__ == "__main__":
    asyncio.run(crawl())
