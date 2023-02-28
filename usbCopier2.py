import os
import shutil
import time
import win32com.shell.shell as shell
import argparse
import sys


def run_as_admin():
    """
    Run the script as administrator.
    """
    if not shell.IsUserAnAdmin():
        shell.ShellExecuteEx(
            lpVerb="runas",
            lpFile=sys.executable,
            lpParameters=" ".join(sys.argv),
            nShow=shell.SW_SHOWNORMAL,
        )
        sys.exit()


def copy_files(usb_drive_path, dest_folder):
    """
    Copy files from the USB drive to the destination folder.
    """
    if os.path.exists(usb_drive_path):
        print("USB drive detected!")
        usb_files = os.listdir(usb_drive_path)
        for file in usb_files:
            if file != "System Volume Information":
                file_path = os.path.join(usb_drive_path, file)
                dest_path = os.path.join(dest_folder, file)
                if os.path.isdir(file_path):
                    try:
                        shutil.copytree(file_path, dest_path)
                    except FileExistsError:
                        shutil.copytree(file_path, dest_path, dirs_exist_ok=True)
                else:
                    shell.ShellExecuteEx(
                        lpVerb="runas",
                        lpFile="cmd.exe",
                        lpParameters='/c copy "{}" "{}"'.format(file_path, dest_path),
                    )
        print("Files copied successfully.")


def main():
    parser = argparse.ArgumentParser(
        description="Automatically copy files from a USB drive to a destination folder.\n\nExample: python usb_copier.py -u F:/ -o C:/temp/usb_content/"
    )
    parser.add_argument("-u", "--usb_path", dest="usb_drive_path", required=True, help="Path to the USB drive")
    parser.add_argument("-o", "--output", dest="dest_folder", required=True, help="Path to the destination folder")
    args = parser.parse_args()

    before = os.listdir(args.dest_folder)

    while True:

    	copy_files(args.usb_drive_path, args.dest_folder)
    	after = os.listdir(args.dest_folder)
    	if before != after:
        	print("Copying complete.")
        	break
    	time.sleep(2)


if __name__ == "__main__":
    run_as_admin()
    main()
