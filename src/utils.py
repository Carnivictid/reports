""" The following are my JSON labels.

["technician"]["name"]
["technician"]["email"]

["technician"]["clients"][X]    # X is index for each client
["technician"]["clients"][X]["name"]

["technician"]["clients"][X]["emails"][Y]   # Y is index for each agent group
["technician"]["clients"][X]["emails"][Y]["subject"]
["technician"]["clients"][X]["emails"][Y]["filename"]

["technician"]["clients"][X]["contacts"][Y] # Y is index for users getting report
["technician"]["clients"][X]["contacts"][Y]["name"]
["technician"]["clients"][X]["contacts"][Y]["email"] 
"""

import json, sys


Backup_Score_mid = "The backup score needs some work. I will open an investigative ticket to resolve any issues with the current backup set.\n\n"
Disk_Score_mid = "The disk score needs some work. There are computers in your system whose drives are nearing full. The attached document shows the workstations' individual disk scores. I would like to schedule time this week or next to find out if we need to clear space from the drives or possibly upgrade them.\n\n"
Patch_Score_mid = "The patch score needs some work. I will audit your workstations and see which machines need patches installed. While we get this list in order, it would help if you could have your employees keep their computers powered on over the next few days. This will allow our system to push patches to the workstations. If any servers need patching, I will work with you to schedule their subsiquent reboots.\n\n"


def open_json(path):
    with open(path, "r") as f:
        return json.loads(f.read())


def main():
    jcontents = open_json("config.json")

    for client in jcontents["technician"]["clients"]:
        print(client["name"])
        for email in client["emails"]:
            print("--"+email["subject"])
        print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
