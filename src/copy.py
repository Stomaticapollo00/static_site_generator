import os, shutil

from nodeconverter import markdown_to_html_node, extract_title

def get_public_dir():
    #Retrieve Public Directory and return it
    current_dir = os.path.dirname(os.path.abspath(__file__))
    public_dir = os.path.join(current_dir, "..", "docs")
    return os.path.abspath(public_dir)

def del_dir(path):
    #Delete given path
    if os.path.exists:
        shutil.rmtree(path)
        print(f"Deleting all of {os.path.basename(path)} directory.")
    else:
        print(f"No dir found at {path}")

def copy_recursive(src, dst):
    #Copy all items (files and directories) from source to destination
    if not os.path.exists(src):
        raise Exception(f"Filepath not found: {src}")
    if not os.path.exists(dst):
        os.mkdir(dst)
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        elif os.path.isdir(src_path):
            os.mkdir(dst_path)
            copy_recursive(src_path, dst_path)

def copy(path):
    #Get Public Directory - delete to clear contents and remake
    public_dir = get_public_dir()
    if os.path.basename(public_dir) != "docs":
        raise Exception("Issue with locating public directory")
    del_dir(public_dir)
    print(f"{os.path.basename(public_dir)} directory has been deleted. Recreating directory.")
    os.mkdir(public_dir)
    print(f"{os.path.basename(public_dir)} directory has been recreated. Copying files from {os.path.basename(path)} directory.")
    
    #Use helper to recursively copy files from source to Public_Directory
    copy_recursive(path, public_dir)
    print(f"All files copied from {os.path.basename(path)} directory.")

def generate_page_helper(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {os.path.basename(from_path)} to {os.path.basename(dest_path)} using {os.path.basename(template_path)}.")
    #Read Markdown file
    with open(from_path, "r", encoding="utf-8") as f:
        md_file = f.read()
    #Read Template for creating output file
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
    
    #Convert Markdown to HTML format
    node = markdown_to_html_node(md_file)       #HTML Nodes
    content = node.to_html()                    #HTML String
    title = extract_title(md_file)              #Heading
    
    #Add Title and Content to file output
    html_file = template.replace("{{ Title }}", title)
    html_file = html_file.replace("{{ Content }}", content)
    
    #Reference Base-path
    html_file = html_file.replace('href="/', f'href="{basepath}')
    html_file = html_file.replace('src="/', f'src="{basepath}')
    
    #Create directories and HTML file in the Destination-path
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(html_file)

def generate_pages(from_path, template_path, dest_path, basepath):
    #Recursively check to generate pages from all files in directory
    if os.path.isdir(from_path):
        for item in os.listdir(from_path):
            item_path = os.path.join(from_path, item)
            if os.path.isfile(item_path):
                item_html = item.replace(".md", ".html")
                new_dest = os.path.join(dest_path, item_html)
            else:
                new_dest = os.path.join(dest_path, item)
            generate_pages(item_path, template_path, new_dest, basepath)
    #Use helper to generate the HTML file
    else:
        generate_page_helper(from_path, template_path, dest_path, basepath)
        

