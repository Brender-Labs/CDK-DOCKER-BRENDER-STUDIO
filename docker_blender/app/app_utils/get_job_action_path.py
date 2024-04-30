def get_job_action_path(job_action):
    script_paths = {
        "copy_efs": "/app/storage_actions/job_1/s3_to_efs.py",
        "clean_efs": "/app/storage_actions/job_3/efs_to_s3.py",
        "render": "/app/render/render_config.py",
    }
    return script_paths.get(job_action, None)