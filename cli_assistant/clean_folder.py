import sys
import shutil
from pathlib import Path

# Create rule of chanding cyrillic letters to latin letters
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ?<>,!@#[]#$%^&*()-=; "
TRANSLATION = (
    "a",
    "b",
    "v",
    "g",
    "d",
    "e",
    "e",
    "j",
    "z",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "r",
    "s",
    "t",
    "u",
    "f",
    "h",
    "ts",
    "ch",
    "sh",
    "sch",
    "",
    "y",
    "",
    "e",
    "yu",
    "ya",
    "je",
    "i",
    "ji",
    "g",
    "_",
    "_",
    "_",
    "_",
    "_",
    "_",
    "_",
    "_",
    "_",
    "_",
    "_",
    "_",
    "_",
    "_",
    "_",
    "_",
    "_",
    "_",
    "_",
    "_",
    "_",
)

TRANS = {}

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name):
    """Change cyrillic letters to latin letters"""
    return name.translate(TRANS)


# Dictionary for set the rules of sorting files
extensions = {
    "images": [".jpeg", ".png", ".jpg", ".svg"],
    "video": [".avi", ".mp4", ".mov", ".mkv"],
    "documents": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"],
    "music": [".mp3", ".ogg", ".wav", ".amr"],
    "archives": [".zip", ".gz", ".tar"],
    "unknown": [""],
}


def create_folders(path: Path):
    """Checking for existing extensions folder. Create if not exist"""
    for name in extensions.keys():
        if not path.joinpath(name).exists():
            path.joinpath(name).mkdir()


def sort_files(path: Path):
    """Pattern "**/*" recursively walk a directory
    for searching all files including folders"""
    for obj in path.glob("**/*"):
        flag = True
        for i in [
            "images",
            "video",
            "documents",
            "music",
            "archives",
            "unknown",
        ]:  # script to ignore these folders
            if i in str(obj):
                flag = False
                break
        """ Chanding cyrillic letters to latin letters and rename file """
        if obj.is_file() and flag is not False:
            file = obj.with_name(normalize(obj.stem)).with_suffix(obj.suffix)
            obj.rename(file)

            """ Check extension of files and sort it"""
            if file.suffix in extensions["images"]:
                img_folder = path / "images"
                lst_img = []
                if img_folder.exists():
                    for f in img_folder.iterdir():
                        lst_img.append(f.name)
                    if file.name in lst_img:
                        add_name = f"_({str(len(lst_img))})"
                        new_file = file.with_name(file.stem + add_name).with_suffix(
                            file.suffix
                        )
                        file.rename(new_file)
                        new_file.replace(img_folder / new_file.name)
                    else:
                        file.replace(img_folder / file.name)

            elif file.suffix in extensions["video"]:
                video_folder = path / "video"
                lst_vd = []
                if video_folder.exists():
                    for f in video_folder.iterdir():
                        lst_vd.append(f.name)
                    if file.name in lst_vd:
                        add_name = f"_({str(len(lst_vd))})"
                        new_file = file.with_name(file.stem + add_name).with_suffix(
                            file.suffix
                        )
                        file.rename(new_file)
                        new_file.replace(video_folder / new_file.name)
                    else:
                        file.replace(video_folder / file.name)

            elif file.suffix in extensions["documents"]:
                doc_folder = path / "documents"
                lst_doc = []
                if doc_folder.exists():
                    for f in doc_folder.iterdir():
                        lst_doc.append(f.name)
                    if file.name in lst_doc:
                        add_name = f"_({str(len(lst_doc))})"
                        new_file = file.with_name(file.stem + add_name).with_suffix(
                            file.suffix
                        )
                        file.rename(new_file)
                        new_file.replace(doc_folder / new_file.name)
                    else:
                        file.replace(doc_folder / file.name)

            elif file.suffix in extensions["music"]:
                msc_folder = path / "music"
                lst_msc = []
                if msc_folder.exists():
                    for f in msc_folder.iterdir():
                        lst_msc.append(f.name)
                    if file.name in lst_msc:
                        add_name = f"_({str(len(lst_msc))})"
                        new_file = file.with_name(file.stem + add_name).with_suffix(
                            file.suffix
                        )
                        file.rename(new_file)
                        new_file.replace(msc_folder / new_file.name)
                    else:
                        file.replace(msc_folder / file.name)

            elif file.suffix in extensions["archives"]:
                arch_folder = path / "archives"
                lst_arch = []
                if arch_folder.exists():
                    for f in arch_folder.iterdir():
                        lst_arch.append(f.name)
                    if file.name in lst_arch:
                        add_name = f"_({str(len(lst_arch))})"
                        new_file = file.with_name(file.stem + add_name).with_suffix(
                            file.suffix
                        )
                        file.rename(new_file)
                        new_file.replace(arch_folder / new_file.name)
                    else:
                        file.replace(arch_folder / file.name)

            else:
                unknown_folder = path / "unknown"
                lst_unk = []
                if unknown_folder.exists():
                    for f in unknown_folder.iterdir():
                        lst_unk.append(f.name)
                    if file.name in lst_unk:
                        add_name = f"_({str(len(lst_unk))})"
                        new_file = file.with_name(file.stem + add_name).with_suffix(
                            file.suffix
                        )
                        file.rename(new_file)
                        new_file.replace(unknown_folder / new_file.name)
                    else:
                        file.replace(unknown_folder / file.name)


def delete_folders(path: Path):
    """Delete all empty folders.
    Pattern "*/**" recursively walk a directory
    for searching only folders. With [::-1] start walk from deepest level"""
    for f in list(path.glob("*/**"))[::-1]:
        if f.is_dir:
            try:
                f.rmdir()
            except OSError:
                pass


def unpack_archives(path: Path):
    """Unpacking archive"""
    path_folder = path / "archives"
    if path_folder.exists():
        for f in path_folder.iterdir():
            try:
                shutil.unpack_archive(f, path_folder / f.stem)
            except:
                print(f"WARNING. {f.name} cannot be unpacked")
            finally:
                continue
    else:
        pass


def main():
    path = None
    try:
        path = Path(sys.argv[1])
        print(f"Start sorting files in folder: {path}")
    except IndexError:
        print("Please enter valid path")

    create_folders(path)
    sort_files(path)
    delete_folders(path)
    unpack_archives(path)
    print("Done")


if __name__ == "__main__":
    main()
