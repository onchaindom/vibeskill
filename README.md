# vibe

The Claude Code plugin that lets you actually vibe while Claude works. Curate a playlist of media via links and Claude creates a locally hosted lounge experience for you tailored to the estimated work time of Claude's session.

## Install

Add the marketplace and install the plugin:

```
/plugin marketplace add Cache-Atelier/vibeskill
/plugin install vibe@cache-atelier
```

## Usage

In Claude Code:

```
/vibe
```

Or just ask naturally:

```
put on some music
I need some focus tunes
```

## How it works

1. Claude estimates how long your task will take
2. Picks media from the playlist
3. Runs `scripts/vibe_lounge.py` to generate an HTML lounge page
4. Opens it in your browser — embedded YouTube player, countdown timer, playlist
5. Gets to work on your task

## Add your own vibes

Create a JSON file in `plugins/vibe/vibes/` following the schema in `plugins/vibe/vibes/vibes.schema.json`:

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
      "duration_minutes": null
    }
  ]
}
```

Set `duration_minutes` to `null` for livestreams.

## Share vibes

This project uses GitHub's fork network for sharing:

1. Fork this repo
2. Add your playlists to `plugins/vibe/vibes/`
3. Push to your fork
4. Others discover your vibes through the fork network

See `plugins/vibe/references/community.md` for more details.

## Manual usage

```bash
python3 plugins/vibe/scripts/vibe_lounge.py --duration 30 --vibes-file plugins/vibe/vibes/default.json
```

Options:
- `--duration` — session length in minutes (default: 30)
- `--vibes-file` — path to a vibes JSON file (repeatable)
- `--output` — output HTML path (default: `/tmp/vibe-lounge.html`)

## Requirements

- Python 3.7+
- A web browser
- Claude Code (for the skill integration)

## License

MIT
