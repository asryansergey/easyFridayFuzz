import os
import subprocess
import sys
import random
import shutil
import argparse
import time

CYCLE_COUNT = 1000
COV_BB = set()
queue_dir = ""

ALPHABET = "abcdefghijklmnopqrstuvwxyz1234567890"


def is_crashing(proc):
    if proc.returncode:
        print("\n[!] CRASH DETECTED")
        return True
    return False


def get_input_from_queue(out_dir):
    pass


def get_coverage():
    pass


def get_random_file():
    queue_len = len(os.listdir(queue_dir))
    rand_num = random.randint(0, queue_len - 1)
    curr_queue_elem = os.path.join(queue_dir, f"current_input: {rand_num}")
    return curr_queue_elem


def replace_random_single_chr(in_text):
    rand_idx = random.randint(0, len(in_text) - 1)
    rand_char = str(random.choice(ALPHABET))
    text = in_text[:rand_idx] + rand_char + in_text[rand_idx + 1 :]
    return text


def create_file_in_queue(content, file_idx):
    new_file_name = f"current_input: {file_idx}"
    queue_new_elem = os.path.join(queue_dir, new_file_name)
    with open(queue_new_elem, "w") as wf:
        wf.write(content)
    return queue_new_elem


def mutate_in(idx):
    rand_queue_file = get_random_file()
    with open(rand_queue_file, "r") as rf:
        cont = rf.readline()

    mutate_cont = replace_random_single_chr(cont)
    print(f"Current text ==> {mutate_cont}")

    new_file_name = create_file_in_queue(mutate_cont, idx)
    return new_file_name


def create_curr_input(input, idx):
    dest = os.path.join(queue_dir, f"current_input: {idx}")
    shutil.copy(input, dest)
    return dest


def run_fuzz(bin, input):
    create_curr_input(input, 0)
    for it in range(1, CYCLE_COUNT):
        curr_in = mutate_in(it)
        proc = subprocess.Popen([bin, curr_in])
        proc.communicate()
        if is_crashing(proc):
            return 1
        time.sleep(0.15)
    return 0


def create_out_dir(out_dir):
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.mkdir(out_dir)


def create_queue_dir(out_dir):
    global queue_dir
    queue_dir = os.path.join(out_dir, "queue")
    if os.path.exists(queue_dir):
        shutil.rmtree(queue_dir)
    os.mkdir(queue_dir)


def parse_argv():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inpur-file", dest="input_file", required=True)
    parser.add_argument("-o", "--output-dir", dest="out_dir", required=True)
    parser.add_argument("-b", "--binary", dest="binary", required=True)
    args = parser.parse_args()
    return args


def main():
    cmdline = parse_argv()
    create_out_dir(cmdline.out_dir)
    create_queue_dir(cmdline.out_dir)
    if run_fuzz(cmdline.binary, cmdline.input_file):
        print("[!] Processes finished successfully")
    else:
        print("\n[-] Process finished with no crashing results")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Process Terminated")
