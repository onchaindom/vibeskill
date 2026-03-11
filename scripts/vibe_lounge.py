#!/usr/bin/env python3
"""Generate a vibe lounge HTML page and open it in the browser."""

import argparse
import json
import random
import signal
import sys
import threading
import webbrowser
from datetime import datetime, timezone
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = SCRIPT_DIR.parent / "assets" / "lounge_template.html"


def load_vibes(paths):
    """Load and merge vibes from one or more JSON files."""
    entries = []
    for p in paths:
        path = Path(p)
        if not path.exists():
            print(f"warning: vibes file not found: {path}", file=sys.stderr)
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            entries.extend(data.get("entries", []))
        except (json.JSONDecodeError, KeyError) as e:
            print(f"warning: skipping malformed vibes file {path}: {e}", file=sys.stderr)
    return entries


def filter_by_mood(entries, mood):
    """Filter entries by mood tag. Falls back to all entries if no matches."""
    if not mood:
        return entries
    filtered = [e for e in entries if mood.lower() in [t.lower() for t in e.get("tags", [])]]
    if not filtered:
        print(f"warning: no entries match mood '{mood}', using all entries", file=sys.stderr)
        return entries
    return filtered


def select_media(entries, duration):
    """Select media to cover the duration.

    Small curated playlists (<=10 entries) are returned in full.
    For larger playlists, greedy-fill preserving order.
    """
    if len(entries) <= 10:
        return list(entries)

    selected_set = set()

    # Always include untimed / browsable entries
    for e in entries:
        if e.get("duration_minutes") is None:
            selected_set.add(id(e))

    # Greedy-fill timed content to cover duration
    if duration:
        covered = 0
        for e in entries:
            if e.get("duration_minutes") is None:
                continue
            if covered >= duration:
                break
            selected_set.add(id(e))
            covered += e["duration_minutes"]

    # Preserve original order from the JSON
    selected = [e for e in entries if id(e) in selected_set]

    if not selected and entries:
        selected = entries[:3]

    return selected


def generate(vibes_json, duration, mood, working_dir, output_path):
    """Read template, substitute placeholders, write output."""
    if not TEMPLATE_PATH.exists():
        print(f"error: template not found at {TEMPLATE_PATH}", file=sys.stderr)
        sys.exit(1)

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    html = template.replace("{{VIBES_JSON}}", json.dumps(vibes_json))
    html = html.replace("{{DURATION_MINUTES}}", str(duration))
    html = html.replace("{{MOOD}}", mood or "")
    html = html.replace("{{WORKING_DIR}}", working_dir)
    html = html.replace("{{GENERATED_AT}}", now)

    output = Path(output_path)
    output.write_text(html, encoding="utf-8")
    return output


def main():
    parser = argparse.ArgumentParser(description="Generate a vibe lounge page")
    parser.add_argument(
        "--duration",
        type=int,
        default=30,
        help="Session duration in minutes (default: 30)",
    )
    parser.add_argument(
        "--vibes-file",
        action="append",
        dest="vibes_files",
        help="Path to a vibes JSON file (repeatable)",
    )
    parser.add_argument(
        "--mood",
        type=str,
        default=None,
        help="Filter by mood tag (e.g. lofi, jazz, ambient)",
    )
    parser.add_argument(
        "--working-dir",
        type=str,
        default=None,
        help="Working directory to display (default: current dir shortened with ~)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="/tmp/vibe-lounge.html",
        help="Output HTML path (default: /tmp/vibe-lounge.html)",
    )
    args = parser.parse_args()

    # Default vibes file
    if not args.vibes_files:
        default_vibes = SCRIPT_DIR.parent / "vibes" / "default.json"
        args.vibes_files = [str(default_vibes)]

    # Load, filter, select
    entries = load_vibes(args.vibes_files)
    if not entries:
        print("error: no vibes entries found", file=sys.stderr)
        sys.exit(1)

    entries = filter_by_mood(entries, args.mood)
    selected = select_media(entries, args.duration)

    # Resolve working directory
    if args.working_dir:
        working_dir = args.working_dir
    else:
        cwd = str(Path.cwd())
        home = str(Path.home())
        if cwd.startswith(home):
            working_dir = "~" + cwd[len(home):]
        else:
            working_dir = cwd

    # Generate
    output = generate(selected, args.duration, args.mood, working_dir, args.output)
    print(str(output))

    # Serve via localhost (YouTube embeds require http://, not file://)
    serve_and_open(output)


def serve_and_open(html_path):
    """Serve the HTML file on a local HTTP server and open it in the browser."""
    html_path = html_path.resolve()
    serve_dir = html_path.parent
    filename = html_path.name

    handler = partial(QuietHandler, directory=str(serve_dir))

    # Find an available port
    server = HTTPServer(("127.0.0.1", 0), handler)
    port = server.server_address[1]

    url = f"http://127.0.0.1:{port}/{filename}"
    print(f"serving lounge at {url}", file=sys.stderr)

    # Run server in a background thread
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    webbrowser.open(url)

    # Keep alive until interrupted
    signal.signal(signal.SIGINT, lambda *_: sys.exit(0))
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    try:
        signal.pause()
    except AttributeError:
        # signal.pause() not available on Windows
        threading.Event().wait()


class QuietHandler(SimpleHTTPRequestHandler):
    """HTTP handler that suppresses request logs."""
    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    main()
