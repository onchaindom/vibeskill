# Community Vibes — Fork Model

## How sharing works

`vibe` uses GitHub's fork network for community sharing. There's no central registry — just repos.

### Share your vibes

1. Fork the repo
2. Add your playlists to `vibes/` (follow `vibes.schema.json`)
3. Push to your fork
4. Others discover your vibes through GitHub's fork network

### Use someone else's vibes

1. Find a fork with playlists you like
2. Download their JSON files into your local `vibes/` directory
3. Or add their fork as a git remote and cherry-pick

### Convention

- Name your playlist files descriptively: `synthwave.json`, `classical-focus.json`, `rain-sounds.json`
- Use tags consistently — check existing playlists for common tags before inventing new ones
- Keep entries to real, working URLs — test your embeds before sharing

## Future ideas

- A community index (curated list of notable forks)
- Tag-based discovery across forks
- A CLI command to fetch playlists from other forks
