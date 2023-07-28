#!/bin/bash

if [ "$#" -lt 2 ]; then
    echo "---------------------------"
    echo "- Snapshot creator script - "
    echo "---------------------------"
    echo "Slow    - name /path/to/backup -s"
    echo "           Encryption + compression + deletion"
    echo "Fast    - name /path/to/backup -f"
    echo "           Encryption only + update diff"
    echo "Restore - name /path/to/backup -r"
    echo "           Restore mode (Careful!)"
    exit
fi

restore=0
fast=0
sync_flags="aAXv"
d=$(date +%s)
backup_path=$1
write_path="~/dec/$2"

check_status()
{
    retVal=$?
    if [ $retVal -ne 0 ]; then
        echo "Error"
        fusermount -u ~/decrypted
        exit $retVal
    fi
}

ask()
{
    read -p $1 -n 1 -r
    echo ""

    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Canceling.."
        exit(0)
    fi
}

if [ "$#" -eq 3 ]; then
    if [ $3 == "-f" ]; then
        fast=1
        write_path="~/dec/fast_snapshot"
    elif [ $3 == "-r" ];
        restore=1
    fi
    sync_flags="aAXvu"
fi

if [ $restore -eq "1" ]; then
    ask "This will restore snapshot from $1, continue? [Y/N] - " 
    
    echo "Mounting encrypted folder.."
    encfs $backup_path/enc ~/dec
    check_status

    # Start syncing    
    echo "Restoring snapshot. Please wait .."
    rsync -$sync_flags $1/* / &> /dev/null
    check_status

    echo "Unmounting encrypted snapshots.."
    fusermount -u ~/decrypted
else 
    ask "This will create encrypted snapshot at $1, continue? [Y/N] - " 
    echo "Creating encrypted partition if not exists.."
    mkdir -p $backup_path/enc ~/dec

    echo "Mounting encrypted folder.."
    encfs $backup_path/enc ~/dec
    check_status

    echo "$(date)"
    echo "Creating snapshot at $write_path.."

    # Start syncing
    echo "Syncing folders. Please wait .."
    rsync -$sync_flags --exclude={"/dev/*","/proc/*","/sys/*","/tmp/*","/run/*","/mnt/*","/media/*","/lost+found","/home"} /* $write_path &> /dev/null

    echo "Additional folders .."
    rsync -$sync_flags /home/$whoami/.config $write_path &> /dev/null
    check_status

    if [ $fast -ne 1 ]; then
        # Compress backup
        echo "Starting compression. please wait.."
        tar -czvf $write_path.tar.gz $write_path &> /dev/null
        check_status

        # Remove non-compressed
        echo "Removing temp folder .."
        rm -rf $write_path &> /dev/null
    fi

    echo "Unmounting encrypted snapshots.."
    fusermount -u ~/decrypted

    echo "Done. Snapshot generated into - $write_path ."
fi
