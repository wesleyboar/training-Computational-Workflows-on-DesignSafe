# connect_tapis()

***connect_tapis(token_filePath="~/.tapis_tokens.json", base_url="https://designsafe.tapis.io", username="", password="", force_connect=False)***

**Purpose.** Create and return an authenticated **Tapis** client (for example, for **DesignSafe**) using **automatic token caching**. When possible, the function reuses a valid saved token so you do not have to log in repeatedly. If no valid token is available, it securely prompts for credentials, fetches a new token, saves it, and returns a ready-to-use client.



### What it does

- **Checks** `token_filePath` (default: `~/.tapis_tokens.json`) for a saved token.
- If a **valid token** is found and `force_connect=False`, it is reused immediately.
- If the token file is **missing**, **expired**, **invalid**, or if `force_connect=True`, the function performs a **fresh login**.
- After a successful fresh login, the function **saves the new token** back to the token file for future use.
- The function prints:
  - whether authentication used a **saved token** or a **fresh login**
  - the token expiration time
  - the remaining time until expiration

### Interactive login behavior

If a fresh login is needed:

- If the `username` argument is empty, you are prompted for it.
- A **blank username** cancels the login and the function returns `None`.
- You are then prompted for the password using a secure hidden prompt.
- A **blank password** restarts the login flow so you can re-enter the username.

This restart behavior is useful if you realize you mistyped the username.

### Parameters

- **token_filePath** *(str, default `"~/.tapis_tokens.json"`)*  
  Path to the JSON file used to store the cached access token and its expiration time.

- **base_url** *(str, default `"https://designsafe.tapis.io"`)*  
  Base URL for the target Tapis tenancy.

- **username** *(str, default `""`)*  
  Username for login. If left blank, the function prompts for it.

- **password** *(str, default `""`)*  
  Password for login. If left blank, the function prompts securely for it. Entering a blank password at the prompt restarts the login flow.

- **force_connect** *(bool, default `False`)*  
  If `True`, ignores any valid saved token and forces a fresh login.



### Returns

* **Tapis client** (`tapipy.tapis.Tapis`) **or `None`**

Returns an authenticated Tapis client on success. Returns `None` if login is cancelled or cannot be completed.



### Token file format (JSON)

```json
{
  "access_token": "…",
  "expires_at": "2025-08-31T12:34:56+00:00"
}
```

Expiry strings are parsed leniently:
* timestamps ending in Z are treated as UTC
* naive timestamps are also assumed to be UTC

On successful fresh login, the function attempts to set the token file permissions to 0600 as a best-effort security measure.


### Notes

* The token file stores the **access token** and **expiry time**, not the password.
* If the saved token cannot be read or validated, the function automatically falls back to a fresh login.
* On success, the function prints one of the following messages:

```text
-- AUTHENTICATED VIA SAVED TOKEN --
```

or

```text
-- AUTHENTICATED VIA FRESH LOGIN --
```

---

### Examples

```python
# Use a saved token if valid; otherwise prompt and save a new one
t = connect_tapis()
if t:
    jobs = t.jobs.getJobList()
    for j in jobs:
        print(j.id, j.status)
```

Force a fresh login (rotate the token):

```python
t = connect_tapis(force_connect=True)
```

Provide credentials programmatically (no prompts on success):

```python
t = connect_tapis(username="me@example.org", password="********")
```

Custom token cache path (e.g., project workspace):

```python
t = connect_tapis(token_filePath="./.secrets/tapis_token.json")
```

Handle a cancelled login gracefully:

```python
t = connect_tapis()
if t is None:
    print("Login cancelled by user.")
```

Fix a mistyped username during prompts:

* At the **password** prompt, press **Enter** with a blank password → you’ll be re-prompted for the username and can try again.

---

### Notes & tips

* **Security:** The token file contains only the access token and expiry, not your password; the code attempts to set file permissions to `0600` after writing.
* **Portability:** You can point *token_filePath* to a project-local location (e.g., inside a shared workspace) if appropriate.
* **Diagnostics:** On success you’ll see `-- AUTHENTICATED VIA SAVED TOKEN` (cache) or `-- AUTHENTICATED VIA FRESH LOGIN`. Expiry time and remaining duration are printed.

---

#### Files

You can find these files in Community Data.

````{dropdown} connect_tapis.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/connect_tapis.py
:language: none
````
