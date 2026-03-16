def connect_tapis(token_filePath: str = "~/.tapis_tokens.json",
                  base_url: str = "https://designsafe.tapis.io",
                  username: str = "",
                  password: str = "",
                  force_connect: bool = False):
    """
    Authenticate to a Tapis tenancy (such as DesignSafe) using cached tokens
    when available, with an interactive login fallback.

    Behavior
    --------
    - Checks ``token_filePath`` (default: ``~/.tapis_tokens.json``) for a saved
      access token and expiry timestamp.
    - If a valid cached token is found and ``force_connect=False``, it is reused
      without prompting for credentials.
    - If the token file is missing, unreadable, invalid, expired, or
      ``force_connect=True``, the function performs a fresh login and saves a
      new token to ``token_filePath``.
    - During interactive login:
      * If ``username`` is empty, you are prompted for it.
      * Entering a blank username cancels login and returns ``None``.
      * You are then prompted for the password.
      * Entering a blank password restarts the login flow so you can re-enter
        the username.
    - Prints token expiry information and whether authentication used a saved
      token or a fresh login.

    Parameters
    ----------
    token_filePath : str, optional
        Path to the JSON file used to store the cached token. The file stores
        values like:
        ``{"access_token": "...", "expires_at": "...ISO8601..."}``.
        Defaults to ``"~/.tapis_tokens.json"``.
    base_url : str, optional
        Base URL of the Tapis tenancy. Defaults to
        ``"https://designsafe.tapis.io"``.
    username : str, optional
        Username to use for login. If empty, the function prompts for it.
        Defaults to ``""``.
    password : str, optional
        Password to use for login. If empty, the function prompts securely for
        it. Entering a blank password at the prompt restarts the login flow so
        the username can be corrected. Defaults to ``""``.
    force_connect : bool, optional
        If ``True``, skips any valid cached token and forces a fresh login.
        Defaults to ``False``.

    Returns
    -------
    tapipy.tapis.Tapis or None
        An authenticated Tapis client if login succeeds, otherwise ``None`` if
        login is cancelled or cannot be completed.

    Notes
    -----
    - Expiry timestamps are parsed leniently. Strings ending in ``"Z"`` are
      treated as UTC, and naive timestamps are assumed to be UTC.
    - On successful fresh login, the token file is written to disk and the code
      attempts to set file permissions to ``0600`` as a best-effort protection.
    - If a saved token cannot be parsed or validated, the function falls back
      to a fresh login.

    Examples
    --------
    Reuse a cached token if valid, otherwise prompt for login:

    >>> t = connect_tapis()
    >>> if t:
    ...     print(t.jobs.getJobList())

    Force a fresh login:

    >>> t = connect_tapis(force_connect=True)

    Provide credentials programmatically:

    >>> t = connect_tapis(username="me@example.org", password="********")

    Cancel login:
    - At the username prompt, press Enter on a blank username.

    Restart login to correct the username:
    - At the password prompt, press Enter on a blank password.

    Author
    ------
    Silvia Mazzoni (silviamazzoni@yahoo.com)

    Date
    ----
    2026-03-16

    Version
    -------
    1.3
    """


    
    from tapipy.tapis import Tapis
    from getpass import getpass
    from datetime import datetime, timezone
    import json
    import os
    from typing import Optional

    def _parse_expires_at(s: str) -> Optional[datetime]:
        """Parse ISO8601 expiry, accepting 'Z' and naive strings; return aware UTC dt or None."""
        if not s:
            return None
        try:
            s_norm = s.replace("Z", "+00:00")
            dt = datetime.fromisoformat(s_norm)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        except Exception:
            return None

    def getTokensLoop(u=None):
        """Prompt repeatedly until tokens are obtained.
        Blank password restarts and re-prompts username. Blank username cancels.
        """
        while True:
            if not u:
                u = getpass("Username (leave blank to cancel): ")
            if u == "":
                print(" Blank username entered → cancelling!!")
                return None
            p = getpass(f"Password for {u} (leave blank to re-enter username): ")
            if p == "":
                print(" Blank password entered → restarting (you can correct the username).")
                u=None
                continue
            t_local = Tapis(base_url=base_url, username=u, password=p)
            try:
                t_local.get_tokens()
                return t_local
            except Exception as e:
                print(f" ** Warning ** could NOT get token : {e}\n TRY AGAIN!")

    print(" -- Checking Tapis token --")
    token_path = os.path.expanduser(token_filePath)
    now = datetime.now(timezone.utc)

    t = None
    saved_expires_at = None
    used_saved_token = False

    # Try to load a saved token unless forcing fresh login
    if force_connect:
        print(" Forcing a connection to Tapis (fresh login).")
    else:
        if os.path.exists(token_path):
            try:
                with open(token_path, "r") as f:
                    tokens = json.load(f)
                saved_expires_at = _parse_expires_at(tokens.get("expires_at"))
                if tokens.get("access_token") and saved_expires_at and saved_expires_at > now:
                    print(" Token loaded from file. Token is still valid!")
                    t = Tapis(base_url=base_url, access_token=tokens["access_token"])
                    used_saved_token = True
                else:
                    print(" Token file found but token is missing/expired.")
                    if saved_expires_at:
                        print(" Token expired at:", saved_expires_at.isoformat())
            except Exception as e:
                print(f" Could not read/parse token file ({token_path}): {e}")
        else:
            print(" No saved tokens found.")

    # If no valid token, perform login
    if t is None:
        print("-- Connect to Tapis --")
        print(" Leave username blank to cancel.")
        if not username:
            username = getpass("Username: ")
        if username == "":
            print(" Login aborted: Blank Username!")
            return None

        if not password:
            password = getpass(f"Password for {username} (leave blank to re-enter username): ")
            if password == "":
                print(" Blank password entered → restarting full login prompts.")
                t = getTokensLoop()
                if t is None:
                    print(" Login aborted.")
                    return None
            else:
                t = Tapis(base_url=base_url, username=username, password=password)
                try:
                    t.get_tokens()
                except Exception as e:
                    print(f" ** Warning ** could NOT get token : {e}\n TRY AGAIN!")
                    t = getTokensLoop(username)
                    if t is None:
                        print(" Login aborted.")
                        return None
        else:
            t = Tapis(base_url=base_url, username=username, password=password)
            try:
                t.get_tokens()
            except Exception as e:
                print(f" ** Warning ** could NOT get token : {e}\n TRY AGAIN!")
                t = getTokensLoop(username)
                if t is None:
                    print(" Login aborted.")
                    return None

        # Save the new token back to the chosen path
        try:
            tokens = {
                "access_token": t.access_token.access_token,
                "expires_at": t.access_token.expires_at.isoformat(),
            }
            parent = os.path.dirname(token_path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(token_path, "w") as f:
                json.dump(tokens, f)
            try:
                os.chmod(token_path, 0o600)  # best-effort tighten perms
            except Exception:
                pass
            print(f" Token saved to {token_path}")
            saved_expires_at = _parse_expires_at(tokens["expires_at"])
        except Exception as e:
            print(f" Warning: could not save token to {token_path}: {e}")

    # Print expiry info
    exp_to_show = saved_expires_at
    try:
        if getattr(t, "access_token", None) and getattr(t.access_token, "expires_at", None):
            exp_to_show = _parse_expires_at(str(t.access_token.expires_at)) or exp_to_show
    except Exception:
        pass

    if exp_to_show:
        print(" Token expires at:", exp_to_show.isoformat())
        print(" Token expires in:", str(exp_to_show - now))
    else:
        print(" Token expiry time unavailable.")

    print("-- AUTHENTICATED VIA {} --".format("SAVED TOKEN" if used_saved_token else "FRESH LOGIN"))
    return t
