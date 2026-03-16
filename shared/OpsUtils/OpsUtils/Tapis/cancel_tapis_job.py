def cancel_tapis_job(tapis_client, job_uuid):
    """
    Request cancellation of a Tapis job by UUID and report its current status.

    Behavior
    --------
    - Calls ``tapis_client.jobs.cancelJob(jobId=job_uuid)`` to request job
      cancellation.
    - If the cancellation request succeeds, immediately queries the job again
      using ``tapis_client.jobs.getJob(jobId=job_uuid)`` and returns the
      reported status.
    - Prints status and diagnostic messages during execution.
    - If an exception occurs, checks for a few common error conditions and
      prints a more specific message when possible.

    Parameters
    ----------
    tapis_client : tapipy.tapis.Tapis
        An authenticated Tapis client.
    job_uuid : str
        UUID of the Tapis job to cancel.

    Returns
    -------
    str or None
        The current reported job status after the cancellation request, such as
        ``"CANCELLED"``, ``"FINISHED"``, ``"FAILED"``, or another Tapis job
        state. Returns ``None`` if the job could not be cancelled or an error
        occurred.

    Notes
    -----
    - A successful cancellation request does not guarantee that the returned
      status will immediately be ``"CANCELLED"``. Depending on timing and job
      state, the job may still report another status when queried right after
      the request.
    - If the job is already complete or already cancelled, Tapis may raise an
      error such as ``"Invalid job state"``.
    - If the UUID is invalid or the job does not exist, Tapis may raise an
      error such as ``"Job not found"``.

    Examples
    --------
    Cancel a job and inspect the returned status:

    >>> status = cancel_tapis_job(t, "abc123-your-job-uuid")
    >>> print(status)

    Handle a failed cancellation attempt:

    >>> status = cancel_tapis_job(t, "bad-or-missing-job-id")
    >>> if status is None:
    ...     print("Cancellation failed.")

    Author
    ------
    Silvia Mazzoni (silviamazzoni@yahoo.com)

    Date
    ----
    2026-03-16

    Version
    -------
    1.1
    """
    
    try:
        # Attempt to cancel the job
        tapis_client.jobs.cancelJob(jobId=job_uuid)
        print(f"Job {job_uuid} cancellation requested...")

        # Confirm the updated job status
        job_status = tapis_client.jobs.getJob(jobId=job_uuid).status
        print(f"✅ Current job status: {job_status}")

        return job_status

    except Exception as e:
        # Handle known issues
        error_message = str(e)

        if "Job not found" in error_message:
            print(f"## Error ##: Job {job_uuid} not found. Check the UUID.")
        elif "Invalid job state" in error_message:
            print(f"** Warning **: Job {job_uuid} may already be completed or cancelled.")
        else:
            print(f"Unexpected error cancelling job {job_uuid}: {error_message}")

        return None
