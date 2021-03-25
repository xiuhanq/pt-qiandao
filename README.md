# 介绍
PT站自动签到工具

# 免责声明
在使用本工具前请认真阅读以下声明:
1. 本工具只限于个人研究学习使用,请勿拿去做任何商业用途
2. 本工具完全基于selenium来实现模拟用户签到动作,签到时不会将数据传送给任何的服务器.
3. 如果因为你个人的作弊而被ban号,跟作者无关.
4. 使用本工具造成的一切损失,与作者无关。如不接受此条款，请不要使用并立刻删除已经下载的源码.
5. 不是python和爬虫科班出身,代码很挫勿喷.

> 目录
- [介绍](#介绍)
- [免责声明](#免责声明)
  - [原理](#原理)
  - [需要安装的包](#需要安装的包)
    - [1. selenium](#1-selenium)
    - [2. yaml配置文件读取组件](#2-yaml配置文件读取组件)
    - [3. 日志框架](#3-日志框架)
    - [4. 定时任务框架](#4-定时任务框架)
    - [5. 安装图片处理器PIL](#5-安装图片处理器pil)
    - [6 安装百度API](#6-安装百度api)
    - [配置文件说明](#配置文件说明)

## 原理
1. 基于selenium调用远程chrome浏览器,模拟用户签到动作.
2. 使用前先自行准备一个远程的可以访问的chrome服务.

## 需要安装的包
### 1. selenium
`python3 -m pip install selenium`
### 2. yaml配置文件读取组件
`python3 -m pip install pyyaml`
### 3. 日志框架
`python3 -m pip install loguru`
### 4. 定时任务框架
`python3 -m pip install apscheduler`
### 5. 安装图片处理器PIL
`python3 -m pip install pillow`
### 6 安装百度API
`python3 -m pip install baidu-aip`

### 配置文件说明 
将`config.yaml`文件放在工具相同目录下
```
qiandao:
  command_executor: 'http://{host}:{port}/wd/hub'   #selenium调用的远程chrome地址
  cron:                                             #增加定时任务配置 每天的 {hour:minute}这个时间会执行一次定时任务
    hour: 20                                        #每天的几点开始
    minute: 30                                      #配合hour 每天的几点几分开始
  image_captcha_save_path: '{path}'                 #缓存验证码图片的文件目录
  qiyeweixin: '{url}'                               #企业微信推送消息机器人地址
  baidu:                                            #百度AI 用于自动识别验证码
    APP_ID: ''
    API_KEY: ''
    SECRET_KEY: ''
  sites:                                            #站点信息列表,可以自行添加多个站点
    - site_name: ''                                 #站点名称
      index_url: ''                                 #首页地址url
      index_url_str: 'index'                        #首页地址url内任意的关键词
      index_btn_xpath: ''                           #登录后跳转首页的按钮的xpath
      login_url: ''                                 #登录地址url
      login_url_str: 'login'                        #登录地址url内任意的关键词
      username_input_xpath: ''                      #登录页面用户名输入框的xpath
      password_input_xpath: ''                      #登录页面密码输入框的xpath
      login_image_captcha_xpath: ''                 #登录页面验证码图片的xpath(如无验证码可空)
      login_image_captcha_input_xpath: ''           #登录页面验证码输入框的xpath(如无验证码可空)
      login_captcha_length:                         #登录页面验证码的长度(如无验证码可空)
      submit_btn_xpath: ''                          #登录页面提交按钮的xpath
      attendance_btn_xpath: ''                      #签到按钮的xpath
      attendance_text: ''                           #签到按钮文字
      username: ''                                  #不用说也知道是啥了吧       
      password: ''                                  #不用说也知道是啥了吧+1
```
>并不完整，如想得到完整配置文件，请自行查看源码 (≧▽≦)/
