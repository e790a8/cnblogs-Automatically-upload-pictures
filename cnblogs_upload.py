#！coding:utf-8
import re
import joblib
import requests
import pathlib

def Data(path):
    with open(file=path,mode="r",encoding="utf-8") as f:
        File_md = f.readlines();
        f.close();
    return File_md

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

def Initialize(args_url,cookie,images_dict):
    Session = requests.Session()
    images_network_dict = Upload_images(session=Session,url=args_url,cookie=cookie,images_dict=images_dict)
    return images_network_dict

def Upload_images(session,url,cookie,images_dict):
    Rule = re.compile(r"\"https://.*\"")
    for i in images_dict:
        suffix = images_dict[i][images_dict[i].rfind("."):]
        img = {"qqfile": (str(i)+suffix, open(images_dict[i], "rb"), "image/"+suffix[1:])}
        html = session.post(url=url, files=img, cookies=cookie)
        Matching = re.search(Rule,html.text)
        if Matching is not None:
            images_dict[i] = Matching.group(0)[1:-1]
    return images_dict

def Change_file(file,images_network_dict):
    for i in images_network_dict:
        file[i] = file[i][:file[i].find("(")+1]+images_network_dict[i]+")"

def main():
    Cookie_file = pathlib.Path("cookie")
    if not Cookie_file.is_file():
        Cnblogs_AspNetCore_Cookies = input(".Cnblogs.AspNetCore.Cookies:")
        CNBlogsCookie = input(".CNBlogsCookie:")
        Cookie = {".Cnblogs.AspNetCore.Cookies": Cnblogs_AspNetCore_Cookies,".CNBlogsCookie": CNBlogsCookie}
        with open(file="cookie",mode="wb") as f:
            joblib.dump(Cookie,f)
            f.close()
    else:
        with open(file="cookie",mode="rb") as f:
            Cookie = joblib.load(f)
            f.close()
    Url = "http://upload.cnblogs.com/imageuploader/processupload?host=www.cnblogs.com&qqfile=name.png"
    while True:
        Path = input("file_path:")
        File_md = Data(path=Path)
        Images_dict = Filtrate_image(file=File_md)
        Images_network_dict = Initialize(args_url=Url,cookie=Cookie,images_dict=Images_dict)
        Change_file(file=File_md,images_network_dict=Images_network_dict)
        with open(file=Path,mode="w",encoding="utf-8") as f:
            f.writelines(File_md)
            f.close()
        print("success!")
        End = input("exit(Y/N):")
        if End == "Y" or End == "y":
            exit(0)

if __name__ == '__main__':
    main()