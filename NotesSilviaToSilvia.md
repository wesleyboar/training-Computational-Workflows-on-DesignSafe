# Notes from Silvia to Silvia
**Working with this repository from the DesignSafe JupyterHub environment**

Personal workflow notes for working with this repository from the  
DesignSafe JupyterHub environment using my fork.
this will likely get updated with time..... let's see

March 2026

These instructions describe how to edit and push changes to this repository while working in the **DesignSafe JupyterHub environment**, using **my personal fork**.

Repository fork:

```
https://github.com/silviamazzoni/training-Computational-Workflows-on-DesignSafe
```

Main repository:

```
https://github.com/DesignSafe-CI/training-Computational-Workflows-on-DesignSafe
```

The workflow is:

JupyterHub → My Fork → Pull Request → Main Repository

---

# 1. GitHub Authentication

GitHub no longer allows account passwords for Git operations.

Before using this repository:

1. Create a **Personal Access Token (PAT)** in GitHub.
2. When Git asks for a password, **enter the PAT instead of your GitHub password**.

You will use this token whenever Git asks for authentication.

---

# 2. Repository Setup (one-time check)

Confirm the repository points to your fork:

```
git remote -v
```

It should show:

```
origin  https://github.com/silviamazzoni/training-Computational-Workflows-on-DesignSafe.git
```

If needed:

```
git remote set-url origin https://github.com/silviamazzoni/training-Computational-Workflows-on-DesignSafe.git
```

---

# 3. Start a Work Session (get latest files)

## Step 1 — Sync your fork in the GitHub browser

Open your fork and click:

```
Sync fork → Update branch
```

This updates your fork with the latest changes from the main DesignSafe repository.

---

## Step 2 — Reset the local JupyterHub clone

Open a **Terminal** in the root of the repository and run:

```
git fetch origin
git reset --hard origin/main
git status
```

This ensures your local files exactly match your fork.

NOTE: This workflow avoids `git pull` because the fork may sometimes be force-updated after PR merges.

---

# 4. Make your edits

Edit files normally.

To see what changed:

```
git status
```

---

# 5. Commit and push changes

Stage the edits:

```
git add .
```

Create a commit:

```
git commit -m "description of the changes"
```

Push to your fork:

```
git push origin main
```

When prompted:

```
Username: silviamazzoni
Password: <enter PAT here>
```

Your changes are now on your fork.

---

# 6. Create the Pull Request

Go to your fork in GitHub.

Click:

```
Compare & Pull Request
```

Create a PR from:

```
silviamazzoni/main
```

to:

```
DesignSafe-CI/main
```

Submit the pull request.

---

# 7. Merge the Pull Request

After submitting the PR, GitHub will take you to the main repository.

Merge the PR there.

Once merged, the changes exist in the **main DesignSafe repository**.

---

# 8. Sync your fork again

Return to your fork in GitHub.

Click:

```
Sync fork
```

If GitHub says the fork is **ahead and behind**, allow the sync and **drop the extra commit**.
This happens because the PR merge already incorporated the change.

---

# 9. Reset the local JupyterHub repo again

Return to the terminal and run:

```
git fetch origin
git reset --hard origin/main
git status
```

Now the local repo matches the fork exactly.

---

# 10. Final State

All three locations should now be synchronized:

| Location               | Status               |
| ---------------------- | -------------------- |
| DesignSafe main repo   | updated              |
| Silvia fork            | synced with upstream |
| JupyterHub local clone | clean and current    |

---

# 11. Quick command summary

Start work session:

```
git fetch origin
git reset --hard origin/main
git status
```

After editing:

```
git add .
git commit -m "message"
git push origin main
```

After PR merge:

```
git fetch origin
git reset --hard origin/main
git status
```

---

# Important Warning

Before running:

```
git reset --hard origin/main
```

ALWAYS check:

```
git status
```

If there are local edits you want to keep, commit them first.




---

# 12. Emergency Recovery

If things look strange, first check:

```bash
git status
git remote -v
git log --oneline --graph --decorate --all -10
```

If you want to throw away local changes and make the JupyterHub copy match your fork exactly:

```bash
git fetch origin
git reset --hard origin/main
git status
```

If Git says the branch has diverged, or `git pull` fails, do **NOT** keep retrying `git pull`.
Instead use:

```bash
git fetch origin
git reset --hard origin/main
git status
```

If you are worried about losing work, make a backup branch first:

```bash
git branch backup-before-reset
git fetch origin
git reset --hard origin/main
git status
```

If you already committed work and want to save it before resetting:

```bash
git branch backup-with-my-work
```

Then reset:

```bash
git fetch origin
git reset --hard origin/main
```

If push fails because the remote changed first, refresh local first:

```bash
git fetch origin
git reset --hard origin/main
```

Then re-apply your edits, commit, and push again.

---

## EMERGENCY RECOVERY

1. Check status:
   git status
   git remote -v
   git log --oneline --graph --decorate --all -10

2. If the repo is confused or git pull fails:
   git fetch origin
   git reset --hard origin/main
   git status

3. If worried about losing work:
   git branch backup-before-reset
   git fetch origin
   git reset --hard origin/main
   git status

DO NOT keep retrying git pull if the branch has diverged.
For this repo, the safe recovery command is:
   git fetch origin
   git reset --hard origin/main

