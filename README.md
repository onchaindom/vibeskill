# vibe

A Claude Code skill that sets the vibe for your coding sessions. Curates ambient music from a playlist, generates an HTML lounge page with embedded players and a countdown timer, opens it in your browser, and gets to work.

## Install

```bash
git clone https://github.com/onchaindom/vibeskill.git ~/.claude/skills/vibe/
```

That's it. The repo root *is* the skill directory.

## Usage

In Claude Code:

```
/vibe
```

Or just ask naturally:

```
put on some music
set the vibe, something jazzy
I need some focus tunes
```

Claude will also auto-trigger before substantial tasks (estimated 10+ minutes).

## How it works

1. Claude estimates how long your task will take
2. Picks media from the playlist, optionally filtered by mood
3. Runs `scripts/vibe_lounge.py` to generate an HTML lounge page
4. Opens it in your browser — embedded YouTube player, countdown timer, playlist
5. Gets to work on your task

The lounge page has a terminal aesthetic: dark background, monospace font, ASCII borders, block-character progress bar.

## Add your own vibes

Create a JSON file in `vibes/` following the schema in `vibes/vibes.schema.json`:

```json
{
  "name": "my-playlist",
  "description": "My custom coding vibes",
  "entries": [
    {
      "title": "Track name",
      "url": "https://www.youtube.com/watch?v=...",
      "embed_url": "https://www.youtube.com/embed/...",
      "platform": "youtube",
      "duration_minutes": null,
      "tags": ["lofi", "chill"]
    }
  ]
}
```

Set `duration_minutes` to `null` for livestreams.

## Share vibes

This project uses GitHub's fork network for sharing:

1. Fork this repo
2. Add your playlists to `vibes/`
3. Push to your fork
4. Others discover your vibes through the fork network

See `references/community.md` for more details.

## Manual usage

```bash
python3 scripts/vibe_lounge.py --duration 30 --vibes-file vibes/default.json --mood lofi
```

Options:
- `--duration` — session length in minutes (default: 30)
- `--vibes-file` — path to a vibes JSON file (repeatable)
- `--mood` — filter by mood tag
- `--output` — output HTML path (default: `/tmp/vibe-lounge.html`)

## Requirements

- Python 3.7+
- A web browser
- Claude Code (for the skill integration)

## License

MIT
