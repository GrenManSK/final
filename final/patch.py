import sys
import os
import shutil
import diff_match_patch as dmp_module
import final.git
import glob
import stat
from subprocess import call
from time import sleep


class patch:
    """
    Only patches that are already on github.com
    """

    def __init__(self, url, patch_version, md_clear=False):
        folder_to_remove = "temp"
        version = patch_version
        self.md_clear = md_clear
        self.url = url
        os.makedirs("temp", exist_ok=True)
        final.git.download(self.url).download("temp").remove_info()

        self.get_patch()

        print("Waiting 2 seconds to clear Access Denied Error")
        sleep(2)
        for i in os.listdir(folder_to_remove):
            if i.endswith("git"):
                tmp = os.path.join(folder_to_remove, i)
                # We want to unhide the .git folder before unlinking it.
                while True:
                    call(["attrib", "-H", tmp])
                    break
                shutil.rmtree(tmp, onerror=on_rm_error)
        print("Waiting 2 seconds to clear Access Denied Error")
        sleep(2)
        shutil.rmtree("temp", onerror=on_rm_error)

        try:
            with open("patch.md", "r") as f:
                patch = f.read()
            if self.md_clear:
                with open("patch.md", "w") as f:
                    pass
        except FileNotFoundError:
            patch = ""
        with open(version, "a") as f3:
            f3.write(f"# {version}\n\n{patch}\n\n```diff\n")
        for file in glob.glob("patch-*.txt"):
            with open(file, "r", encoding="utf-8") as f:
                if (fr := f.read()) != "":
                    name = file
                    with open(version, "a", encoding="utf-8") as f3:
                        if fr == "\n":
                            f.close()
                            os.remove(file)
                            continue
                        f3.write(
                            (
                                (
                                    (
                                        name.replace("patch-temp#29", "").replace(
                                            "#29", "/"
                                        )[:-4]
                                        + "\n"
                                    )
                                    + fr
                                )
                                + "\n"
                            )
                        )

                f.close()
                os.remove(file)
        with open(version, "a") as f3:
            f3.write("```\n")
        os.makedirs("patch_notes", exist_ok=True)
        shutil.move(version, f"patch_notes/{version}.md")

    def get_patch(self, folder="temp"):
        for filename in glob.glob(f"{folder}/*", recursive=True):
            if filename.startswith("patch_notes"):
                continue
            if os.path.isdir(filename):
                self.get_patch(filename)
                continue
            one_file(
                filename, filename.replace("temp\\", ""), filename.replace("\\", "#29")
            )


def readFileToText(filePath):
    try:
        file = open(filePath, "r", encoding="utf-8")
        s = ""
        for line in file:
            s = s + line
        return s
    except FileNotFoundError:
        return "File was removed"
    except UnicodeDecodeError:
        return ""


def one_file(origin, latest, filename):
    dmp = dmp_module.diff_match_patch()

    originText = readFileToText(origin)
    latestText = readFileToText(latest)

    if latestText == "File was removed":
        patchText = "- File was removed"
    else:
        patch = dmp.patch_make(originText, latestText)
        patchText = dmp.patch_toText(patch)

    # folder = sys.argv[1]
    folder = f"patch-{filename}.txt"

    print(folder)
    patchFilePath = folder
    with open(patchFilePath, "w", encoding="utf-8") as patchFile:
        for text in patchText.split("\n"):
            text = (
                text.replace("%22", '"')
                .replace("%25", "%")
                .replace("%5C", "\\")
                .replace("%5B", "[")
                .replace("%5D", "]")
                .replace("%7B", "{")
                .replace("%7D", "}")
            )
            if len(text) > 0:
                if text[0] == "+":
                    patchFile.write(text.replace("%0A", "\n+") + "\n")
                elif text[0] == "-":
                    patchFile.write(text.replace("%0A", "\n-") + "\n")
                else:
                    patchFile.write(text + "\n")
            else:
                patchFile.write("\n")
    patchFile.close()


def on_rm_error(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)
