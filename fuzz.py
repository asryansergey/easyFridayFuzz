import os
import subprocess
import sys
import random
import shutil

cycle_count = 1000;
cov_bb = set()

alphabet = "abcdefghijklmnopqrstuvwxyz1234567890"

def is_crashing(proc):
    if proc.returncode:
        print "\n[!] CRASH DETECTED"
        return True
    return False

def get_input_from_queue(out_dir):
    pass

def get_coverage():
    pass

def mutate_in(in_file):
    with open(in_file, "r") as rf:
        cont = rf.readline()
    text = ""
    for i in range(0,2):
        text += random.choice(alphabet)
    sys.stdout.write("\rCurrent text ==> %s" % text)
    sys.stdout.flush()
    with open(in_file, "w") as wf:
        wf.write(text)

def create_curr_input(input):
    dest = "current_input"
    shutil.copy(input, dest)
    return dest

def run_fuzz(bin, input):
    curr_in = create_curr_input(input)
    for it in range(0, cycle_count):
        proc = subprocess.Popen([bin, curr_in])
        proc.communicate()
        if is_crashing(proc):
            os.remove(curr_in)
            return 1
        mutate_in(curr_in)
    os.remove(curr_in)
    return 0;


def main(bin, input):
    if run_fuzz(bin, input):
        print "[!] Processes finished successfully"
    else:
        print "\n[-] Process finished with no crashing results"

main(sys.argv[1], sys.argv[2])