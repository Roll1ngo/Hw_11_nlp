import subprocess


def main():
    subprocess.check_call(["python", "-m", "spacy", "download", "en_core_web_sm"])


if __name__ == "__main__":
    main()
