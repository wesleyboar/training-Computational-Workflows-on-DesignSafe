# Git-JupyterHub Workflow Notes for This Repo
***Working with this repository from the DesignSafe JupyterHub environment***

**Notes from Silvia to Silvia:**
Personal workflow notes for working with this repository from the
DesignSafe JupyterHub environment using **my fork and an upstream remote**.

This document will likely evolve with time.

March 2026

---

# Repository Locations

My fork:

```
https://github.com/silviamazzoni/training-Computational-Workflows-on-DesignSafe
```

Main repository:

```
https://github.com/DesignSafe-CI/training-Computational-Workflows-on-DesignSafe
```

Workflow:

```
JupyterHub → My Fork → Pull Request → Main Repository
```

---

# 1. GitHub Authentication

GitHub no longer allows account passwords for Git operations.

Before using this repository:

1. Create a **Personal Access Token (PAT)** in GitHub.
2. When Git asks for a password, **enter the PAT instead of your GitHub password**.

So when prompted:

```
Username: yourUserName
Password: <paste PAT>
```

---

# 2. Repository Setup (one-time setup)

Confirm the repository points to your fork:

```
git remote -v
```

You should see:

```
origin  https://github.com/silviamazzoni/training-Computational-Workflows-on-DesignSafe.git
```

If needed:

```
git remote set-url origin https://github.com/silviamazzoni/training-Computational-Workflows-on-DesignSafe.git
```

---

## Add the upstream repository

Add the DesignSafe repository as `upstream`:

```
git remote add upstream https://github.com/DesignSafe-CI/training-Computational-Workflows-on-DesignSafe.git
```

Check:

```
git remote -v
```

You should now see:

```
origin    https://github.com/silviamazzoni/training-Computational-Workflows-on-DesignSafe.git
upstream  https://github.com/DesignSafe-CI/training-Computational-Workflows-on-DesignSafe.git
```

Where:

* **origin** = my fork
* **upstream** = main DesignSafe repository

---

# 3. Start a Work Session (get latest files)

Open a **Terminal in JupyterHub** at the root of the repository and run:

```
git fetch upstream
git checkout main
git reset --hard upstream/main
git push origin main
git status
```

This does four things:

1. pulls the latest changes from the **DesignSafe main repo**
2. makes the **local repo match upstream**
3. updates **my fork** to match upstream
4. confirms the repo is clean

This replaces the older browser-based **Sync fork** step.

---

# 4. Make your edits

Edit files normally.

Check what changed:

```
git status
```

---

# 5. Commit and push changes

Stage edits:

```
git add .
```

Commit:

```
git commit -m "description of the changes"
```

Push to your fork:

```
git push origin main
```

---

# 6. Create the Pull Request

Go to your fork on GitHub and open a PR.

From:

```
silviamazzoni/main
```

To:

```
DesignSafe-CI/main
```

Submit the pull request.

---

# 7. Merge the Pull Request

Merge the PR into the main repository.

After the PR is merged, the main repository now contains the changes.

Your fork may temporarily show:

```
This branch is 1 commit ahead and 1 commit behind
```

This is normal.

---

# 8. Clean up the fork after the merge

Return to **JupyterHub** and run:

```
git fetch upstream
git checkout main
git reset --hard upstream/main
git push --force-with-lease origin main
git status
```

This step:

* updates local repo from upstream
* resets the fork to match upstream
* removes the "ahead / behind" message

Important:

```
git push --force-with-lease
```

is **only used during this cleanup step after a PR merge**.

---

# 9. Final State

After cleanup all three locations are synchronized:

| Location               | Status           |
| ---------------------- | ---------------- |
| DesignSafe main repo   | updated          |
| Silvia fork            | matches upstream |
| JupyterHub local clone | clean            |

---

# 10. Quick command summary

### Start session

```
git fetch upstream
git checkout main
git reset --hard upstream/main
git push origin main
git status
```

### After editing

```
git add .
git commit -m "message"
git push origin main
```

### After PR merge

```
git fetch upstream
git checkout main
git reset --hard upstream/main
git push --force-with-lease origin main
git status
```

---

# Important Warning

Before running:

```
git reset --hard upstream/main
```

always check:

```
git status
```

because `reset --hard` will discard uncommitted tracked changes.

---

# Emergency Recovery

If something looks strange, first check:

```
git status
git remote -v
git log --oneline --graph --decorate --all -10
```

To force your local repo to match the main repository:

```
git fetch upstream
git checkout main
git reset --hard upstream/main
git status
```

To also force your fork to match the main repository:

```
git fetch upstream
git checkout main
git reset --hard upstream/main
git push --force-with-lease origin main
```

If you are worried about losing work:

```
git branch backup-before-reset
```

then run the reset.

---

## Optional Safety Setting

To prevent accidental problematic `git pull` behavior in this repo, run:

```bash
git config pull.ff only
````

This makes `git pull` fail unless it is a simple fast-forward.
That is useful because this workflow uses `fetch + reset` instead of `pull`.

What it does:
* if you accidentally type git pull, Git will only allow the pull if it can be done as a simple fast-forward
* if the histories diverged, Git will stop instead of trying to invent a merge/rebase situation

That is useful for your workflow because you are now intentionally using:
```bash
git fetch upstream
git checkout main
git reset --hard upstream/main
```
instead of relying on git pull.

So this setting acts like a guardrail. It helps prevent Git from doing something messy if you forget and type git pull.

If you want it only for this repo, run:
```bash
git config pull.ff only
```
If you wanted it for all repos on that machine, it would be:
```bash
git config --global pull.ff only
```
For your DesignSafe repo, I would use the repo-only version.




There is also another option:

```bash
git config pull.rebase false
````

but in your case `pull.ff only` is the cleaner safety net.

