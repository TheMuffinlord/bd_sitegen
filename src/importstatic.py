from blockfuncs import *
from htmlnode import *
from textnode import *
from loosefunctions import *

import os, datetime, shutil

def log_timestamp(open_file, text:str): #i'm so tired of typing these two instructions
    now = datetime.datetime.now()
    if text.endswith("\n"):
        text = text.rstrip("\n")
    open_file.write(f"{now}: {text}\n")

def import_from_static(logfile, pub_dir): #takes a file path as input for log file destination
    with open(logfile, "a", encoding="utf-8") as l:
        log_timestamp(l, "beginning import from static to public. stand back.\n==================================\n")
        pub_check = os.listdir(".")
        if pub_check.count(pub_dir) != 0:
            if os.path.isdir(pub_dir):
                log_timestamp(l, "deleting items from public folder\n")
                deleted = delete_from_path(logfile, pub_dir)
                if deleted == False:
                    log_timestamp(l, "delete may not have completed cleanly. check directory\n")
                else:
                    if os.listdir(".").count(pub_dir) == 0:
                        os.mkdir(pub_dir)
                        log_timestamp(l, "public cleared, remaking and moving on")
                    else:
                        log_timestamp(l, "public wasn't cleared but we'll go on anyway.")
            elif os.path.isfile(pub_dir):
                os.remove(pub_dir)
                log_timestamp(l, "somehow public was a file. moving on now")
        else:
            log_timestamp(l, "no public exists, moving on to copy")
            os.mkdir(pub_dir)
        log_timestamp(l, "copying files from static to public")

        copy_files(logfile, "static", pub_dir)
        log_timestamp(l, "COMPLETE: operation should be done. phew!\n==================================")

    l.closed
    print("copy process completed. check log for details.")


def delete_from_path(logfile, path):
    with open(logfile, "a", encoding="utf-8") as l:
        removed_folder = False
        path_list = os.listdir(path)
        if path_list == []:
            os.rmdir(path)
            log_timestamp(l, f"REMOVED folder {path} on initial check: empty folder\n") #the simplest log file of all time
            return True
        else:
            for p in path_list:
                checkpath = f"{path}/{p}"
                if checkpath.find(".") == -1:
                    removed_folder = delete_from_path(logfile, checkpath)
                    if removed_folder == False:
                        os.rmdir(checkpath)
                        log_timestamp(l, f"REMOVED folder {checkpath} once empty\n")
                        removed_folder = True
                else:
                    os.remove(checkpath)
                    log_timestamp(l, f"REMOVED file {checkpath}\n")
                    if removed_folder != True:
                        removed_folder = False
        if path_list == []:
            os.rmdir(path)
            log_timestamp(l, f"REMOVED folder {path} on clear, empty folder\n") 
            return True
    l.closed
    return removed_folder


def copy_files(logfile, o_path, d_path):
    with open(logfile, "a", encoding="utf-8") as l:
        origin_list = os.listdir(o_path)
        if origin_list == []:
            log_timestamp(l, f"COPY: no files to write from directory {o_path}\n")           
        else:            
            for o_item in origin_list:
                d_item = f"{d_path}/{o_item}"
                original_item = f"{o_path}/{o_item}"
                if os.path.isdir(original_item):
                    os.makedirs(d_item)
                    log_timestamp(l, f"COPY: created directory {d_item}, adding items\n")
                    copy_files(logfile, original_item, d_item)
                elif os.path.isfile(original_item):
                    shutil.copy(original_item, d_path)
                    log_timestamp(l, f"COPY: copied item {original_item} to {d_path}\n")
                else:
                    log_timestamp(l, f"COPY: i don't know what {original_item} is. not copied")
    l.closed

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")
    from_file = open(from_path)
    template_file = open(template_path)
    from_markdown = from_file.read()
    template_html = template_file.read()
    from_htmlnode = markdown_to_html_node(from_markdown)
    from_html = from_htmlnode.to_html()
    from_title = extract_title(from_markdown).lstrip("# ")
    dest_html = template_html.replace("{{ Title }}", from_title)
    dest_html = dest_html.replace("{{ Content }}", from_html)
    dest_html = dest_html.replace('href="/', f'href="{basepath}')
    dest_html = dest_html.replace('src="/', f'src="{basepath}')
    from_file.close()
    template_file.close()
    with open(dest_path, "w", encoding="utf-8") as dest_file:
        dest_file.write(dest_html)
    dest_file.closed

def convert_md_files(logfile, md_path, dest_path, basepath):
    with open(logfile, "a", encoding="utf-8") as l:
        md_list = os.listdir(md_path)
        if md_list == []:
            log_timestamp(l, f"CONVERT: no files to convert from {md_path}\n")           
        else:            
            for md_item in md_list:
                d_item = f"{dest_path}/{md_item}"
                original_item = f"{md_path}/{md_item}"
                if os.path.isdir(original_item):
                    try:
                        os.makedirs(d_item)
                        log_timestamp(l, f"CONVERT: created directory {d_item}, adding items\n")
                    except FileExistsError:
                        log_timestamp(l, f"CONVERT: directory {d_item} already exists. moving on")
                    
                    convert_md_files(logfile, original_item, d_item, basepath)
                elif os.path.isfile(original_item):
                    if original_item.endswith(".md"):
                        d_item = d_item.replace(".md", ".html")
                        generate_page(original_item, "template.html", d_item, basepath)
                        log_timestamp(l, f"CONVERT: converted item {original_item} to {d_item}\n")
                else:
                    log_timestamp(l, f"CONVERT: {original_item} not converted, only markdown files get converted")
    l.closed