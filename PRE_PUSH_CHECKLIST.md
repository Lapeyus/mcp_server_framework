# Pre-Push Checklist

Use this checklist before pushing changes from this monorepo.

## 1) Workspace Hygiene

- [ ] `git status --short` shows only intended changes.
- [ ] No backup folders, local virtualenvs, or generated caches are included.
- [ ] No secrets or local absolute paths were added.

## 2) Environment

- [ ] Fresh venv is active.
- [ ] Dependencies install successfully:
  - `pip install -r requirements.txt`

## 3) Validation

- [ ] Syntax check passes:
  - `python -m compileall -q mcp_servers mcp_server_client`
- [ ] Start each server entrypoint at least once.
- [ ] Start each client entrypoint at least once.

## 4) Documentation

- [ ] README paths and script names match real files.
- [ ] New modules/scripts include a short usage note.

## 5) Git

- [ ] Commit message explains intent and scope.
- [ ] Branch is rebased/merged with target branch.
- [ ] Final review of `git diff --stat` and `git diff`.
