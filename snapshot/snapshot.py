from enum import Enum
import subprocess
from pathlib import Path
from tools.table import *
import uuid
from datetime import datetime

script_path = "Scripts/take_snapshot.sh"

class SnapshotTable(Table): 
    restore_request = 0
    snapshot_request = 0

    def exec_snapshot_op(uuid, dest, mode):
        print(uuid + " " + dest + " " + mode)
        return subprocess.call(["./" + script_path, uuid, dest, mode])
        

    def exec_snapshot_delete(uuid, dest):
        print("deleting " + uuid + " " + dest)
        return
        try:
            directory = Path(dest)
            for item in dest.iterdir():
                if item.is_dir():
                    rmdir(item)
                else:
                    item.unlink()
            dest.rmdir()
            return 1
        except:
            return 0

    
    def mark_for_op(self, snapshot_uuid, op, op_type):
        row = None
        if (snapshot_uuid != None):
            row, i = self.get_row_by_key_val(SnapshotKeys.Title.name, snapshot_uuid)
        else:
            # create mode, we need new uuid.
            snapshot_uuid = str(uuid.uuid4())
        
        if (op == SnapshotOperation.CREATE.name):
            if (self.snapshot_request == 0):
                # Mark as pending snapshot, prevent multiple requests.
                # Do we execute quick or full snapshot?
                self.snapshot_request = 1
                self.add_row([SnapshotKeys.Title.name, SnapshotKeys.Date.name, SnapshotKeys.Type.name, SnapshotKeys.Status.name],[snapshot_uuid, str(datetime.now()), op_type, SnapshotStatus.PENDING_SNAPSHOT.name]) 

        elif (op == SnapshotOperation.RESTORE.name):
            if (self.restore_request == 0 and row[SnapshotKeys.Status.name] == SnapshotStatus.AVAILABLE.name):
                # Mark as pending restore, prevent multiple requests.
                self.restore_request = 1
                self.edit_col(SnapshotKeys.Title.name, snapshot_uuid, SnapshotKeys.Status.name, SnapshotStatus.PENDING_RESTORE.name)
                # Cancel restore operation
            elif (self.restore_request == 1 and row[SnapshotKeys.Status.name] == SnapshotStatus.PENDING_RESTORE.name): 
                self.restore_request = 0
                self.edit_col(SnapshotKeys.Title.name, snapshot_uuid, SnapshotKeys.Status.name, SnapshotStatus.AVAILABLE.name)

        elif (op == SnapshotOperation.DELETE.name):
            if (row[SnapshotKeys.Status.name] == SnapshotStatus.MARKED_FOR_DELETE.name):
                # already marked, return.
                return
            elif (row[SnapshotKeys.Status.name] == SnapshotStatus.AVAILABLE.name): 
                self.edit_col(SnapshotKeys.Title.name, snapshot_uuid, SnapshotKeys.Status.name, SnapshotStatus.MARKED_FOR_DELETE.name)
                # Available for restoring. mark it.
                return
            elif (row[SnapshotKeys.Status.name] == SnapshotStatus.PENDING_SNAPSHOT.name):
                # Delete a snapshot request? we can request another.
                self.snapshot_request = 0
            elif (row[SnapshotKeys.Status.name] == SnapshotStatus.PENDING_RESTORE.name):
                # Delete a restore request? we can request another.
                self.restore_request = 0
            # Either way we can now remove the request from the table.
            self.remove_row(SnapshotKeys.Title.name, snapshot_uuid)

    
    def execute(self):
        for row in self.data:
            if (row[SnapshotKeys.Status.name] == SnapshotStatus.PENDING_SNAPSHOT.name): 
                self.edit_col(SnapshotKeys.Title.name, row[SnapshotKeys.Title.name], SnapshotKeys.Status.name, SnapshotStatus.UNAVAILABLE.name)
                
                self.edit_col(SnapshotKeys.Title.name, row[SnapshotKeys.Title.name], SnapshotKeys.Status.name, SnapshotStatus.AVAILABLE.name)

            if (row[SnapshotKeys.Status.name] == SnapshotStatus.PENDING_RESTORE.name):
                pass
            if (row[SnapshotKeys.Status.name] == SnapshotStatus.MARKED_FOR_DELETE.name):
                pass
    

class SnapshotOperation(Enum):
    CREATE = 0
    RESTORE = 1
    DELETE = 2

class SnapshotStatus(Enum):
    PENDING_SNAPSHOT = 0
    PENDING_RESTORE = 1
    MARKED_FOR_DELETE = 2
    AVAILABLE = 3
    UNAVAILABLE = 4


class SnapshotType(Enum):
    FULL = 0
    QUICK = 1


class SnapshotKeys(Enum):
    Title = 0
    Type = 1
    Date = 2
    Status = 3


