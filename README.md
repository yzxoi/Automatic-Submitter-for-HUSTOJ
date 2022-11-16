# Automatic Submitter for HUSTOJ

为 HUSTOJ 打造的自动提交机

[![GitHub](https://img.shields.io/github/license/yzxoi/Automatic-Submitter-for-HUSTOJ?color=blue&style=flat-square)](https://github.com/yzxoi/Automatic-Submitter-for-HUSTOJ/blob/master/LICENSE) [![GitHub last commit](https://img.shields.io/github/last-commit/yzxoi/Automatic-Submitter-for-HUSTOJ?style=flat-square)](https://github.com/yzxoi/Automatic-Submitter-for-HUSTOJ/commits/master) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/yzxoi/Automatic-Submitter-for-HUSTOJ?style=flat-square)

## 特性

- **自动化** - 使用 Selenium with Python 实现自动化交题
- **同步化** - 支持自动爬取大号提交记录以提交至小号
- **定制化** - 支持自定义选择题目提交
- **连续化** - 支持避免提交已经通过的题

## 开始

Tips: 推荐使用 Python 3.10+ 版本构建运行。

0. 安装 Python 及依赖库：
```shell
$ choco install python
$ pip install selenium
$ pip install requests
$ pip install lxml
```

下载符合自己浏览器版本的 [chromedriver](https://chromedriver.chromium.org/downloads)，并加入 PATH 路径。

1. 打开终端，运行：
```shell
$ git clone https://github.com/yzxoi/Automatic-Submitter-for-HUSTOJ.git
```
2. 修改 main.py 内的配置文件:
```shell
$ vi Automatic-Submitter-for-HUSTOJ/main.py
```
3. 运行 main.py：
```shell
$ python main.py
```

## 配置

1. 填写 HUSTOJ 网址 URL。
2. 填写主账号提交者 MAIN_SUBMITTER。该账号应含有**某一种语言**所有**正确**提交记录。
3. 填写提交语言 LANGUAGE。（对应代码表见[附录](#%E9%99%84%E5%BD%95)）
4. 填写子账号(bot 账号) USER_ID。
5. 填写子账号(bot 账号) PASSWORD。
6. 填写主账号 Cookie：替换 `<cookie>`。
7. 子账号必须**至少提交一题**。

```python
URL = "http://syzoj.hustoj.com/"
MAIN_SUBMITTER = "std"
LANGUAGE = "6"
USER_ID = "spider"
PASSWORD = "spider123456"

headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
	"Cookie": "<cookie>"
}
```

### cookie 查找方法：

登录主账号，打开 F12 开发者管理工具，打开控制台 Console，输入：

```
document.cookie
```

其所返回的字符串即为 cookie。

**注意当运行本程序时要确保主账号处于登录状态。**

## 附录

| 语言 | 代码 |
| :----- | :----- |
| C | 0 |
| C++ | 1 |
| Java | 3 |
| Python | 6 |
| PHP | 7 |
| C# | 9 |
| JavaScript | 16 |
| Go | 17 |
| SQL | 18 |
