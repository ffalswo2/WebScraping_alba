from albamon import get_jobs as get_albamon
from albaheaven import get_jobs as get_albaheaven
from save import save_to_file


# albamon = get_albamon()
albaheaven = get_albaheaven()

jobs = albaheaven

save_to_file(jobs)