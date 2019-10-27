import subprocess

def play(filename):
    cmd = f"afplay {filename}"
    subprocess.call(cmd.split(" "))

if __name__ == "__main__":
    play("assets/type4.m4a")
