# Advanced Usage

This file documents advanced, internal-only controls. Normal users never need these — the skill handles composition automatically. Only use these for backward compatibility or precise production control.

## Layout Override

Layout (the internal composition structure of a poster) is selected automatically from content goal, information density, visual subject, channel, and aspect ratio. Users do not see or choose layouts in the normal flow.

Advanced users may force a specific internal layout with `--layout <id>`:

```bash
/poster-generator path/to/content.md --style swiss-editorial --layout modular-grid
```

Rules:

- The value must exactly match the basename of one definition file in `references/layouts/` (for example, `modular-grid` matches `references/layouts/modular-grid.md`; do not include `.md`).
- An explicit override takes precedence over automatic selection, does not change style or other output options, and must not be silently replaced.
- If the value is invalid, stop before rendering and list the valid IDs.
- When `--layout` is active, do not rerun automatic composition selection if the aspect ratio changes.
- An active `--layout` override is reported in the final summary as `Advanced layout override: <id>` for auditability.

A legacy layout preference in EXTEND.md is also honored with the same validation rules, but should not be offered as a normal user setting.
