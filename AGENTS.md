# Website work

Every visual change must follow `design-system/REFERENCE.md` and pass `python3 design-system/style-lint.py`.

Run linter tests with `python3 -m unittest discover -s design-system -p 'test_*.py'`.
Keep the six public pages in the same printed issue; preserve product facts,
links, anchors, captures, mobile sources, captions, licenses and interactions.

Preview command, when no preview already exists: `python3 -m http.server 4179 --bind 127.0.0.1 --directory docs`.
Use an existing preview without starting or stopping servers. Only `docs/` is
served; design references and canonical screenshots stay in `design-system/`.

Public-repo hygiene: no private absolute paths, private hosts, credentials,
internal reports or reference photographs. Use relative paths in documentation.
Loopback in the preview command is local development only. Nothing pushed
without owner approval; do not publish, deploy or open a PR unless instructed.
