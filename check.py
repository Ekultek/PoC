import re
import os
import subprocess


def check_for_write(file_path):
    """
    check if we have write access to the file
    """
    return os.access(file_path, os.R_OK)


def check_versions():
    """
    check the systemctl version and the polykit version
    """
    max_version_ctl = "239"
    max_version_poly = "115"
    data_ctl = subprocess.check_output(["systemctl", "--version"])
    data_poly = subprocess.check_output(["pkttyagent", "--version"])
    results_ctl = data_ctl.split(" ")
    results_poly = data_poly.split(" ")
    vnum_ctl = results_ctl[1].split("\n")[0]
    vnum_poly = results_poly[-1].split(".")[-1]
    if vnum_ctl <= max_version_ctl:
        if vnum_poly <= max_version_poly:
            return True
        else:
            return False
    return False


def check_for_uid(file_path):
    retval = []
    max_int = 294967296
    searcher = re.compile(r"\b(\d+)\b")
    with open(file_path) as data:
        for line in data.readlines():
            if searcher.search(line) is not None:
                splitter = line.split(":")
                uid = splitter[2]
                try:
                    if int(uid) >= max_int:
                        retval.append(line.strip())
                except:
                    pass
    if len(retval) != 0:
        return retval
    else:
        return None


def main():
    file_path = "/etc/passwd"

    if check_versions():
        print("[+] version number is within attack scope")
        write_access = check_for_write(file_path)
        if write_access:
            print("[+] it appears that there is write access to '/etc/passwd'")
            possible_compromises = check_for_uid(file_path)
            if possible_compromises is not None:
                print("[+] there is a total of {} possible compromised user(s):".format(len(possible_compromises)))
                for item in possible_compromises:
                    print(item)
            else:
                print("[-] no users are compromised at this time")
                print("[+] the system is vulnerable and you have the ability to manually create a user")
        else:
            print("[x] there is no write access to /etc/passwd, not possible to manually create a compromised user")
    else:
        print("[x] version appears to be patched against attack")


if __name__ == "__main__":
    main()