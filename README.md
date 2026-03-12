# vibe

The Claude Code skill that lets you actually vibe while Claude works. Curate a playlist of media via links and Claude creates a locally hosted lounge experience for you tailored to the estimated work time of Claude's session. 

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
can you spin up the vibe lounge for me while you work?
if that's going to take a while, let me vibe in the meantime
```

Claude will also auto-trigger before substantial tasks (estimated 10+ minutes).

## How it works

1. Claude estimates how long your task will take
2. Picks media from the playlist
3. Runs `scripts/vibe_lounge.py` to generate an HTML lounge page
4. Opens it in your browser — embedded YouTube player, countdown timer, playlist
5. Gets to work on your task

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


## License

MIT
