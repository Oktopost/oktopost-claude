# Contributing to oktopost-claude

Thank you for your interest in contributing to the Oktopost skill for Claude. This guide covers everything you need to get started.

## Reporting bugs

Open a [GitHub Issue](https://github.com/Oktopost/oktopost-claude/issues) with:

- A clear, descriptive title
- Steps to reproduce the problem
- Expected vs. actual behavior
- Your environment (OS, Node version, Claude Code version)

## Requesting features

Open a [GitHub Issue](https://github.com/Oktopost/oktopost-claude/issues) and add the **enhancement** label. Describe the use case, not just the solution you have in mind.

## Submitting pull requests

1. **Fork** the repository and create a branch from `main`.
2. Make your changes in a focused, well-scoped branch.
3. Test the full flow before submitting (see *Testing* below).
4. Open a pull request against `main` with a clear description of what changed and why.
5. One approval is required before merging.

## Development setup

```bash
# Clone your fork
git clone https://github.com/<you>/oktopost-claude.git
cd oktopost-claude

# Run the installer in local-dev mode
bash install.sh

# Test with Claude Code
claude
```

No additional package managers or dependencies are required. The project is designed to work with Claude Code's built-in tooling.

## Code style

- **Python scripts** use the standard library only -- no pip dependencies. This ensures the skill runs on any machine with Python 3.8+.
- **Markdown** follows the formatting conventions already established in the repo. Use ATX-style headings, fenced code blocks, and keep lines readable.
- **JSON** files use 2-space indentation.

## Testing

Before submitting a PR that touches skill logic, test the full lifecycle:

1. Run `install.sh` to install the skill locally.
2. Run `setup` workflow to confirm preset loading works.
3. Run at least one additional workflow (e.g., Publishing or Analytics) end-to-end.

If your change is documentation-only, a quick review for formatting and accuracy is sufficient.

## License

By contributing, you agree that your contributions will be licensed under the [Apache License 2.0](LICENSE), the same license that covers this project.
