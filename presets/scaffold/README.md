# My Preset

A custom preset for Spec Kit. Copy this directory and customize it to create your own.

## What this scaffold provides

**Active by default** — these install cleanly with no extra dependencies:

| Name | Type | Strategy | Description |
|------|------|----------|-------------|
| `spec-template` | template | replace | Full override of the core spec template |
| `speckit.specify` | command | replace | Full override of the core specify command |
| `plan-template` | template | append | Adds a Compliance & Sign-off section after the core plan template |

**Opt-in examples** — commented out in `preset.yml`; uncomment one only when its prerequisite is installed (otherwise the override has nothing to compose with):

| Name | Type | Needs | Description |
|------|------|-------|-------------|
| `myext-template` | template | the `myext` extension | Override an extension-provided template |
| `speckit.myext.myextcmd` | command | the `myext` extension | Override an extension-provided command |
| `speckit.specify` (wrap) | command | — | Wrap a command with a preamble/sign-off via `{CORE_TEMPLATE}` |

## Development

1. Copy this directory: `cp -r presets/scaffold my-preset`
2. Edit `preset.yml` — set your preset's ID, name, description, and templates
3. Add or modify templates in `templates/`
4. Test locally: `specify preset add --dev ./my-preset`
5. Verify resolution: `specify preset resolve spec-template` (and `plan-template`, etc.)
6. Remove when done testing: `specify preset remove my-preset`

> **There is no `specify preset validate`.** `specify preset resolve <name>` *is* the check:
> run it for every entry you declare. If an override targets a base that isn't present (e.g. an
> extension template you don't have installed), it resolves to nothing — that's how you catch a
> dead override before publishing.

## Manifest Reference (`preset.yml`)

Required fields:
- `schema_version` — always `"1.0"`
- `preset.id` — lowercase alphanumeric with hyphens
- `preset.name` — human-readable name
- `preset.version` — semantic version (e.g. `1.0.0`)
- `preset.description` — brief description
- `requires.speckit_version` — version constraint (e.g. `>=0.1.0`)
- `provides.templates` — list of templates with `type`, `name`, and `file`

## Template Types

- **template** — Document scaffolds (spec-template.md, plan-template.md, tasks-template.md, etc.)
- **command** — AI agent workflow prompts (e.g. speckit.specify, speckit.plan)
- **script** — Custom scripts (reserved for future use)

## Choosing a strategy

Each entry composes with the lower-priority version (core, or an extension) using one of four
strategies (default `replace`). Pick the lightest one that does the job:

| Strategy | Use when… | Your file contains | Survives upstream changes? |
|----------|-----------|--------------------|----------------------------|
| `replace` | You want full control and don't care about future core edits | The whole template/command | No — you own it entirely |
| `append` | You only need to **add** sections (e.g. a compliance block) | Just the added content | Yes — core changes flow through |
| `prepend` | You need content **before** the core (e.g. a preamble/banner) | Just the added content | Yes |
| `wrap` | You need to surround core content (preamble **and** sign-off) | A wrapper with `{CORE_TEMPLATE}` (or `$CORE_SCRIPT`) where core goes | Yes |

Prefer `append`/`prepend`/`wrap` over `replace` when you can: they keep inheriting upstream
improvements instead of freezing a copy. (Scripts support only `replace` and `wrap`.)

## Publishing

See the [Preset Publishing Guide](../PUBLISHING.md) for details on submitting to the catalog.

## License

MIT
