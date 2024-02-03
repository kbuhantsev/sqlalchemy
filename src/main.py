from queries.orm import SyncOrm
from queries.core import SyncCore

# SyncCore.create_tables()
# SyncCore.insert_workers()
# SyncCore.update_worker(worker_id=2, worker_name="VOLK")
# SyncCore.select_workers()

# SyncOrm.create_tables()
# SyncOrm.insert_workers()
# SyncOrm.update_worker(worker_id=2, worker_name="VOLK")
# SyncOrm.select_workers()

# SyncOrm.insert_resumes()
SyncOrm.select_resumes_avg_compensation()