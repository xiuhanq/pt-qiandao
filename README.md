# 介绍
PT站自动签到工具 

# 免责声明
在使用本工具前请认真阅读以下声明:
1. 本工具只限于个人研究学习使用,请勿拿去做任何商业用途
2. 本工具完全基于selenium来实现模拟用户签到动作,签到时不会将数据传送给任何的服务器.
3. <font color='red'>如果因为你个人的作弊而被ban号,跟作者无关.</font>
4. <font color='red'>使用本工具造成的一切损失,与作者无关。如不接受此条款，请不要使用并立刻删除已经下载的源码.</font>
5. 不是python和爬虫科班出身,代码很挫勿喷. ╮(﹀_﹀”)╭
  
# 目录
- [介绍](#介绍)
- [免责声明](#免责声明)
- [目录](#目录)
  - [版本日志](#版本日志)
  - [原理](#原理)
  - [默认支持站点](#默认支持站点)
  - [需要安装的包](#需要安装的包)
    - [1. selenium](#1-selenium)
    - [2. yaml配置文件读取组件](#2-yaml配置文件读取组件)
    - [3. 日志框架](#3-日志框架)
    - [4. 定时任务框架](#4-定时任务框架)
    - [5. 安装图片处理器PIL](#5-安装图片处理器pil)
    - [6 安装百度API](#6-安装百度api)
  - [配置文件说明](#配置文件说明)
  - [Docker](#docker)
    - [Docker镜像地址](#docker镜像地址)
    - [启动命令](#启动命令)
    - [docker-compose 配置](#docker-compose-配置)
  - [待优化功能](#待优化功能)

## 版本日志
- 1.0.1
  - 企业微信通知内容增加签到文本结果
- 1.0.0
  - 简化配置文件(可自定义覆盖默认配置)
  - 优化README
  - 增加cookies支持
- 0.0.X 初始版本
  - 使用使用python3基础Docker镜像
  - 配合selenium/standalone-chrome Docker镜像使用
  - 配置文件包含所有支持站点信息 


## 原理
1. <font color='blue'>基于selenium调用远程chrome浏览器,模拟用户签到动作.</font>
2. <font color='blue'>本工具需要配合远程chrome一起使用，如何使用远程chrome请自行[百度](https://www.baidu.com)</font>

## 默认支持站点
站点 | 
--- |
海棠(htpt) |
老师站(nicept) |
HDU |
猫站(pterclub)|
家园(hdhome) |
高清时间(hdtime) |
烧包(ptsbao) |
聆音(soulvoice) |
柠檬(lemonhd) |
铂金家(pthome) |
海胆(haidan) |
皇后(opencd) |
杜比视界(hdatmos) <font color=red>只支持cooikes登录</font> |
杜比(hddolby) <font color=red>只支持cooikes登录</font> |
PT时间(pttime) <font color=red>只支持cooikes登录</font> |
> 别问为啥只有这些,问就是没有 ╮(╯▽╰)╭

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

## 配置文件说明 
```
qiandao:
  command_executor: 'http://{host}:{port}/wd/hub'   #selenium调用的远程chrome地址
  cron:                                             #增加定时任务配置 每天的 {hour:minute}这个时间会执行一次定时任务
    hour: 20                                        #每天的几点开始
    minute: 30                                      #配合hour 每天的几点几分开始
  qiyeweixin: '{url}'                               #企业微信推送消息机器人地址
  baidu:                                            #百度AI 用于自动识别验证码
    APP_ID: ''
    API_KEY: ''
    SECRET_KEY: ''
  sites:                                            #站点信息列表,可以自行添加多个站点
    - site_name: ''                                 #站点名称
      username: 'xxxxx'                                       
      password: 'xxxxx'
      cookies: '{cookies_file_name}'                                  
```

> 配置文件内sites参数说明
><table>
> <tr align=center><td>键</td><td>描述 </td><td>必填</td><td>备注</td></tr>
> <tr ><td> site_name </td><td> 站点名称 </td><td align=center> &#10003; </td><td> </td></tr>
> <tr><td> username </td><td> 用户名 </td><td align=center> &#10003; </td><td rowspan=3>用户名密码和cookies两者二选一<br>如果两个都填了以用户名密码为主 <br>如果使用cookies登录,cookies导出后以json格式字符串保存到文本文件中，cookies参数填写文件名称 </td></tr>
> <tr><td> password </td><td> 密码 </td><td align=center> &#10003; </td></tr>
> <tr><td> cookies </td><td> cookies文件名称，内容为json格式字符串 </td><td align=center>&#10003;</td></tr>
> <tr><td> index_url </td><td> 首页链接 </td><td align=center> &#10007; </td><td>填写之后会覆盖默认配置</td></tr>
> <tr><td> index_url_str </td><td> 首页链接判断字符串 </td><td align=center> &#10007; </td><td>填写之后会覆盖默认配置</td></tr>
> <tr><td> index_btn_xpath </td><td> 首页按钮xpath选择器 </td><td align=center> &#10007; </td><td>填写之后会覆盖默认配置</td></tr>
> <tr><td> login_url </td><td> 登录链接 </td><td align=center> &#10007; </td><td>填写之后会覆盖默认配置</td></tr>
> <tr><td> login_url_str </td><td> 登录链接判断字符串 </td><td align=center> &#10007; </td><td>填写之后会覆盖默认配置</td></tr>
> <tr><td> username_input_xpath </td><td> 用户名输入框xpath选择器 </td><td align=center> &#10007; </td><td>填写之后会覆盖默认配置</td></tr>
> <tr><td> password_input_xpath </td><td> 密码输入框xpath选择器 </td><td align=center> &#10007; </td><td>填写之后会覆盖默认配置</td></tr>
> <tr><td> login_image_captcha_xpath </td><td> 登录验证码图片xpath选择器 </td><td align=center> &#10007;  </td><td>填写之后会覆盖默认配置</td></tr>
> <tr><td> login_image_captcha_input_xpath </td><td> 登录验证码输入框xpath选择器 </td><td align=center> &#10007; </td><td>填写之后会覆盖默认配置</td></tr>
> <tr><td> login_captcha_length </td><td> 登录验证码校验长度 </td><td align=center> &#10007; </td><td>填写之后会覆盖默认配置</td></tr>
> <tr><td> submit_btn_xpath </td><td> 登录提交按钮xpath选择器 </td><td align=center> &#10007; </td><td>填写之后会覆盖默认配置</td></tr>
> <tr><td> attendance_frame_id </td><td> 签到弹出框frameId</td><td align=center> &#10007; </td><td><font color='red'>opencd用</font><br>填写之后会覆盖默认配置</td></tr>
> <tr><td> attendance_btn_xpath </td><td> 签到按钮xpath选择器 </td><td align=center> &#10007; </td><td>填写之后会覆盖默认配置</td></tr>
> <tr><td> attendance_text </td><td> 签到按钮校验文本 </td><td align=center> &#10007; </td><td>填写之后会覆盖默认配置</td></tr>
> <tr><td> attendance_image_captcha_xpath </td><td> 签到验证码图片xpath选择器 </td><td align=center> &#10007; </td><td>填写之后会覆盖默认配置</td></tr>
> <tr><td> attendance_image_captcha_input_xpath </td><td> 签到验证码输入框xpath选择器 </td><td align=center> &#10007; </td><td>填写之后会覆盖默认配置</td></tr>
> <tr><td> attendance_captcha_length </td><td> 签到验证码校验长度 </td><td align=center> &#10007; </td><td>填写之后会覆盖默认配置</td></tr>
> <tr><td> attendance_submit_btn_xpath </td><td> 签到提交按钮xpath选择器 </td><td align=center> &#10007; </td><td>填写之后会覆盖默认配置</td></tr>
></table>
> 

## Docker
### Docker镜像地址
> [https://hub.docker.com/r/xiuhanq/pt-qiandao](https://hub.docker.com/r/xiuhanq/pt-qiandao)
### 启动命令
```
docker run -d \
--name ptchrome \
--restart always \
-p 5901:5900 \
-p 4444:4444 \
-v /dev/shm:/dev/shm \
selenium/standalone-chrome-debug:latest

docker run -d \
--name pt-qiandao \
-v {your_config_path}:/ptqiandao/config.yaml \         #请修改为自己实际的config文件路径
-v {your_cookies_files_path}:/ptqiandao/cookies_files/  #配合cookies登录时使用,目录为保存各站点cookies文件的目录
--restart always \
xiuhanq/pt-qiandao:latest
```
### docker-compose 配置
```
version: "3.8"
services:
  pt-qiandao:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 64M
    image: xiuhanq/pt-qiandao:latest
    container_name: pt-qiandao
    environment:
      - TZ=Asia/Shanghai
    volumes:
      - {your_config_path}:/ptqiandao/config.yaml # 配置文件路径请修改为自己的config文件
    depends_on:
      - ptchrome
    restart: always
  ptchrome:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 2G
    image: selenium/standalone-chrome-debug:latest
    container_name: ptchrome
    environment:
      - TZ=Asia/Shanghai
    volumes:
      - /dev/shm:/dev/shm
    ports:
      - 5901:5900
      - 4444:4444
    restart: always
```
## 待优化功能
<table>
  <tr>
    <td>状态</td>
    <td>内容</td>
  </tr>
  <tr>
    <td>&#10003;</td>
    <td>优化README</td>
  </tr>
  <tr>
    <td>&#10003;</td>
    <td>简化配置文件</td>
  </tr>
  <tr>
    <td>&#10003;</td>
    <td>任意配置用户名密码登录或者cookies登录</td>
  </tr>  
  <tr>
    <td>&#10003;</td>
    <td>企业微信通知内容增加签到文本结果</td>
  </tr>
<table>


