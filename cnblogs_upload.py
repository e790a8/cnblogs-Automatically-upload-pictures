#！coding:utf-8
import re
import joblib
import requests
import pathlib
import threading
import time

# 检查文件类型是否合格
def Check_path(path):
    suffix = path[path.rfind("."):]
    if suffix == ".md":
        return True
    else:
        return False

# 检查Cookie
def Check_cookie(cookie):
    url = "https://upload.cnblogs.com/imageuploader/upload?host=www.cnblogs.com&editor=4#md-editor"
    html = requests.get(url=url,cookies=cookie)
    if html.text.find("未登录，请先") != -1:
        return False
    else:
        return True

# Cookie
def Return_cookie(Cookie=None):
    Cookie_file = pathlib.Path("cookie")
    if not Cookie_file.is_file():
        Cnblogs_AspNetCore_Cookies = input(".Cnblogs.AspNetCore.Cookies:")
        CNBlogsCookie = input(".CNBlogsCookie:")
        Cookie = {".Cnblogs.AspNetCore.Cookies": Cnblogs_AspNetCore_Cookies, ".CNBlogsCookie": CNBlogsCookie}
        if not Check_cookie(cookie=Cookie):
            print("Cookie Error!")
            Return_cookie(Cookie=Cookie)
        else:
            with open(file="cookie", mode="wb") as f:
                joblib.dump(Cookie, f)
                f.close()
    else:
        with open(file="cookie", mode="rb") as f:
            Cookie = joblib.load(f)
            f.close()
    return Cookie

# 获取文件数据
def Data(path):
    with open(file=path,mode="r",encoding="utf-8") as f:
        File_md = f.readlines();
        f.close();
    return File_md

# 过滤文件内容中的图片链接
def Filtrate_image(file):
    Rule = re.compile(r"\!\[.*\]\(.*\)")
    Images_dict = dict()
    for i in range(len(file)):
        Matching = re.search(Rule,file[i])
        if Matching is not None:
            Rule_file_path = re.compile(r"\(.*\)")
            Matching_file_path = re.search(Rule_file_path, Matching.group(0))
            if Matching_file_path is not None:
                Images_dict[i] = Matching_file_path.group(0)[1:-1]
    return Images_dict

# Session初始化
def Initialize(args_url,cookie,images_dict):
    Session = requests.Session()
    Upload_images(session=Session,url=args_url,cookie=cookie,images_dict=images_dict)
    if Detection_thread():
        return

# 上传图片文件
def Upload_images(session,url,cookie,images_dict):
    Rule = re.compile(r"\"https://.*\"")
    Thread_list = list()
    for i in images_dict:
        suffix = images_dict[i][images_dict[i].rfind("."):]
        img = {"qqfile": (str(i)+suffix, open(images_dict[i], "rb"), "image/"+suffix[1:])}
        td = threading.Thread(target=Thread_upload,args=(i,images_dict,Rule,session,url,img,cookie))
        Thread_list.append(td)
    for t in Thread_list:
        t.start()

# 多线程上传
def Thread_upload(i,images_dict,rule,session,url,img,cookie):
    html = session.post(url=url,files=img,cookies=cookie)
    Matching = re.search(pattern=rule,string=html.text)
    if Matching is not None:
        images_dict[i] = Matching.group(0)[1:-1]
        print(images_dict[i])

# 等待多线程执行完毕
def Detection_thread():
    while True:
        time.sleep(1)
        if threading.active_count() == 1:
            break
    return True


# 新建文件，并保存
def Change_save_file(path,file,images_network_dict):
    try:
        for i in images_network_dict:
            file[i] = file[i][:file[i].find("(")+1]+images_network_dict[i]+")"
        with open(file=path, mode="w", encoding="utf-8") as f:
            f.writelines(file)
            f.close()
        print("Save Success!")
    except:
        print("Save Error!")

def main():
    Cookie = Return_cookie()
    Upload_url = "http://upload.cnblogs.com/imageuploader/processupload?host=www.cnblogs.com&qqfile=name.png"
    while True:
        Path = input("file_path(exit:Y/N):")
        if Path == "Y" or Path == "y":
            exit(0)
        elif not Check_path(path=Path):
            print("FileType Error!")
            continue
        File_md = Data(path=Path)
        Path = Path[:Path.rfind(".")]+"(Copy)"+Path[Path.rfind("."):]
        Images_dict = Filtrate_image(file=File_md)
        Initialize(args_url=Upload_url,cookie=Cookie,images_dict=Images_dict)
        Change_save_file(path=Path,file=File_md,images_network_dict=Images_dict)

if __name__ == '__main__':
    main()