## dsh-client-ui-aqua {{TAG}}

Glassmorphism theme for the **DSH desktop app**.

| | |
|---|---|
| Plugin version | `{{VERSION}}` |
| Supported DSH desktop version | **0.2.1-rc.5** (verified) |
| Platforms | macOS (verified) / Windows (same install path) |
| Install | Plugin Manager → Add plugin → `github:{{REPO}}` |
| Required step | fully quit and reopen the app after installing |

### Attached assets

| Asset | Purpose |
|---|---|
| `client.js` | the shipped client bundle, for auditing or manual comparison |
| `install.ps1` | upstream helper script, kept for provenance only |

### Auto-generated source archives

In addition to the assets above, GitHub attaches **auto-generated**
`Source code (zip)` and `Source code (tar.gz)` archives to every release.
They are produced by GitHub from the tag — not uploaded by this workflow —
and contain the full repository at that exactly pinned revision, which makes
them handy for auditing, archiving, or a fully offline install.

To install from a source archive:

1. Download `Source code (tar.gz)` and extract it
2. Install the extracted directory as a local plugin (absolute path required):

   ```sh
   dsh plugin --profile desktop add link:/absolute/path/to/extracted-directory
   ```

3. Fully quit and reopen the desktop app

**Full changelog:** https://github.com/{{REPO}}/commits/{{TAG}}
