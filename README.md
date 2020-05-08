# 博客园自动上传图片

​	最近用Typora写博客，发现包括博客园在内的其他博客之类的网站，无法一次把文章整体上传，图片需要一张一张的上传，麻烦的要死，所以就萌生了搞个自动上传图片的工具。

# 整体思路

## 寻找上传图片的接口
![image-20200508101830839](https://github.com/lisztomania-Zero/cnblogs-Automatically-upload-pictures/blob/master/%E5%9B%BE%E7%89%87/image-20200508101830839.png)

![image-20200508101855127](https://github.com/lisztomania-Zero/cnblogs-Automatically-upload-pictures/blob/master/%E5%9B%BE%E7%89%87/image-20200508101855127.png)

## 经过抓包发现上传接口

![image-20200508102521047](https://github.com/lisztomania-Zero/cnblogs-Automatically-upload-pictures/blob/master/%E5%9B%BE%E7%89%87/image-20200508102521047.png)

## 编写脚本

大家看代码哈！很简陋的代码，能用。后续再改进。

## 使用方法

python cnblogs_upload.py

.Cnblogs.AspNetCore.Cookies:输入此cookie

.CNBlogsCookie:输入此cookie

file_path:输入文件绝对路径

稍等片刻即可



## 效果展示

![image-20200508105948839](https://github.com/lisztomania-Zero/cnblogs-Automatically-upload-pictures/blob/master/%E5%9B%BE%E7%89%87/image-20200508105948839.png)

![image-20200508110243175](https://github.com/lisztomania-Zero/cnblogs-Automatically-upload-pictures/blob/master/%E5%9B%BE%E7%89%87/image-20200508110243175.png)

![image-20200508110626916](https://github.com/lisztomania-Zero/cnblogs-Automatically-upload-pictures/blob/master/%E5%9B%BE%E7%89%87/image-20200508110626916.png)
