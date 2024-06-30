import os


def write_hrefs(hrefs: list, file_name: str):
    with open(get_file_root_path(f"db/{file_name}"), "a+", newline="\n", encoding="utf8") as f:
        for href in hrefs:
            print(href, file=f)
        print(f'successful write hrefs to {file_name}')


def get_file_content_as_list(name: str):
    job_ids_file = open(get_file_root_path(f"db/{name}"), "r+", encoding='utf8')
    known_job_ids = job_ids_file.read().splitlines()
    job_ids_file.close()
    return known_job_ids


def get_file_root_path(path: str):
    project_root = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(project_root, f"{path}")
