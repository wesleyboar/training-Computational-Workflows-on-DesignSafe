# cancel_tapis_job()
***cancel_tapis_job(tapis_client, job_uuid)***

**Purpose.** Request cancellation of a **Tapis job** by UUID, then immediately query and return the job’s current reported status.

---

### What it does

- Calls `tapis_client.jobs.cancelJob(jobId=job_uuid)` to request job cancellation.
- If that succeeds, immediately calls `tapis_client.jobs.getJob(jobId=job_uuid)` to retrieve the current job status.
- Prints progress and status messages to help with debugging and interactive use.
- Handles a few common error cases, including:
  - job not found
  - invalid job state
  - unexpected exceptions

---

### Parameters

- **tapis_client**  
  An authenticated `tapipy.tapis.Tapis` client.

- **job_uuid** *(str)*  
  UUID of the Tapis job to cancel.

---

### Returns

- **`str` or `None`**

Returns the current reported job status after the cancellation request, such as:

- `CANCELLED`
- `FINISHED`
- `FAILED`

or another Tapis job state.

Returns `None` if the cancellation request fails or an exception occurs.

---

### Important behavior note

A successful cancellation request does **not** necessarily mean the job status will immediately be `CANCELLED`.

Because the function checks status right after requesting cancellation, the returned value may still reflect another state depending on timing, backend processing, or whether the job had already reached a terminal state.

For example:
- a running job may later transition to `CANCELLED`
- a job that already finished may remain `FINISHED`
- a job already in a terminal state may raise an error such as `Invalid job state`

---

### Error handling

The function checks the exception text for a few common cases:

- **`Job not found`**  
  Prints a message indicating the UUID may be incorrect.

- **`Invalid job state`**  
  Prints a warning that the job may already be finished or cancelled.

- **Any other exception**  
  Prints a generic unexpected error message.

In all of these error cases, the function returns `None`.

---

### Example usage

```python
from tapipy.tapis import Tapis

# Assume you already have an authenticated Tapis client
# t = Tapis(base_url="https://designsafe.tapis.io", access_token="your_token_here")

job_id = "abc123-your-job-uuid"
status = cancel_tapis_job(t, job_id)

if status is not None:
    print("Returned status:", status)
else:
    print("Cancellation failed.")
````

---

### Example: pre-check terminal states

If you want, you can check the job status before requesting cancellation:

```python
status = t.jobs.getJob(jobId=job_id).status

if status in ["FINISHED", "FAILED", "CANCELLED"]:
    print(f"Job is already in a terminal state: {status}")
else:
    cancel_tapis_job(t, job_id)
```

---

### Notes

* This function is useful in notebooks and scripts where you want a quick cancellation helper with basic feedback.
* It is intentionally lightweight and does not poll repeatedly for the final terminal state.
* If you need stronger confirmation, you could extend it to poll until the job reaches a terminal status.

---

#### Files

You can find this file in Community Data.

````{dropdown} cancel_tapis_job.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/cancel_tapis_job.py
:language: python
````


