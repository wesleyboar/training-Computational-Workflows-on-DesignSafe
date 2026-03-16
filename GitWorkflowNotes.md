# Git Workflow Notes for This Repo

**DesignSafe JupyterHub + personal fork + upstream repo**

Notes from Silvia in 2026 to Silvia in 20xx


These are my notes for working with this repository from the **DesignSafe JupyterHub environment**.

This workflow uses:

* `origin` = **my fork**
* `upstream` = **the main DesignSafe-CI repository**

Repository URLs:

* My fork: `https://github.com/silviamazzoni/training-Computational-Workflows-on-DesignSafe`
* Main repo: `https://github.com/DesignSafe-CI/training-Computational-Workflows-on-DesignSafe`

The workflow is:

**JupyterHub local repo → my fork (`origin`) → Pull Request → main repo (`upstream`)**

---

## 1. GitHub Authentication

GitHub does **not** use normal account passwords for Git operations.

When Git asks for a password, use a **Personal Access Token (PAT)**.

So when prompted:

* **Username** = `silviamazzoni`
* **Password** = paste the PAT

---

## 2. One-Time Remote Setup

Check the remotes:

```bash
git remote -v
```

They should look like this:

```bash
origin    https://github.com/silviamazzoni/training-Computational-Workflows-on-DesignSafe.git (fetch)
origin    https://github.com/silviamazzoni/training-Computational-Workflows-on-DesignSafe.git (push)
upstream  https://github.com/DesignSafe-CI/training-Computational-Workflows-on-DesignSafe.git (fetch)
upstream  https://github.com/DesignSafe-CI/training-Computational-Workflows-on-DesignSafe.git (push)
```

If `upstream` is missing, add it:

```bash
git remote add upstream https://github.com/DesignSafe-CI/training-Computational-Workflows-on-DesignSafe.git
```

If `origin` is wrong, fix it:

```bash
git remote set-url origin https://github.com/silviamazzoni/training-Computational-Workflows-on-DesignSafe.git
```

---

## 3. Start a Work Session

At the start of each session, update everything from the **main repo** and then update the fork from JupyterHub.

Run:

```bash
git fetch upstream
git checkout main
git reset --hard upstream/main
git push origin main
git status
```

What this does:

* gets the latest changes from the main DesignSafe repo
* makes the local `main` match the main repo exactly
* updates my fork to match the same state
* confirms the repo is clean

This replaces the old browser-based “Sync fork” step.

---

## 4. Make Edits

Edit files normally in JupyterHub.

Check what changed:

```bash
git status
```

---

## 5. Commit and Push to My Fork

After making edits:

```bash
git add .
git commit -m "describe the changes"
git push origin main
```

This sends the changes to my fork.

---

## 6. Open the Pull Request

Go to my fork on GitHub and open a pull request.

PR direction:

* **from:** `silviamazzoni/main`
* **to:** `DesignSafe-CI/main`

Submit the PR.

---

## 7. Merge the Pull Request

Merge the PR into the main DesignSafe repository.

After the PR is merged, the main repo contains the change, but my fork may temporarily show:

> This branch is 1 commit ahead of and 1 commit behind upstream

That is normal.

---

## 8. Clean Up After the Merge

After the PR is merged, go back to **JupyterHub** and resync everything from the main repo.

Run:

```bash
git fetch upstream
git checkout main
git reset --hard upstream/main
git push --force-with-lease origin main
git status
```

What this does:

* updates local `main` to exactly match the main repo
* force-updates my fork to match the same state
* removes the “1 ahead / 1 behind” problem on the fork

### Important

Use:

```bash
git push --force-with-lease origin main
```

**only for this cleanup step after the PR has already been merged.**

Do **not** use it for normal everyday pushes.

---

## 9. Daily Workflow Summary

### Start of session

```bash
git fetch upstream
git checkout main
git reset --hard upstream/main
git push origin main
git status
```

### After making edits

```bash
git add .
git commit -m "message"
git push origin main
```

### After merging the PR

```bash
git fetch upstream
git checkout main
git reset --hard upstream/main
git push --force-with-lease origin main
git status
```

---

## 10. Important Warning About Reset

Before running:

```bash
git reset --hard upstream/main
```

always check:

```bash
git status
```

If there are local changes I want to keep, I must commit them first.

`git reset --hard` will discard uncommitted tracked changes.

---

## 11. Emergency Recovery

If things look strange, check:

```bash
git status
git remote -v
git log --oneline --graph --decorate --all -10
```

If I want to make my local repo match the main repo exactly:

```bash
git fetch upstream
git checkout main
git reset --hard upstream/main
git status
```

If I also want my fork to match the main repo exactly:

```bash
git fetch upstream
git checkout main
git reset --hard upstream/main
git push --force-with-lease origin main
git status
```

If I am worried about losing work, make a backup branch first:

```bash
git branch backup-before-reset
```

Then do the reset.

---

## 12. Key Rule

For this repo:

* use **normal push** during regular work:

```bash
git push origin main
```

* use **force-with-lease** only after the PR is already merged and I am cleaning up my fork:

```bash
git push --force-with-lease origin main
```
