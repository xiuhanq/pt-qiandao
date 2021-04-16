from loguru import logger
import yaml
import os
import requests

class Notify(object):
    # def __init__(self):
    def get_notify_url(self):
        # 获取当前脚本所在文件夹路径
        current_path = os.path.abspath(".")
        # 获取yaml配置文件路径
        yamlPath = os.path.join(current_path, "config.yaml")
        # open方法打开直接读出来
        file = open(yamlPath, 'r', encoding='utf-8')
        # 读出来是字符串
        cfgStr = file.read() 
        # 用load方法转字典
        cfg = yaml.load(cfgStr, Loader=yaml.FullLoader)
        qiandaoCfg = cfg.get('qiandao')
        # logger.info('签到配置文件:{}',str(qiandaoCfg))
        file.close()
        return qiandaoCfg.get('qiyeweixin')
        
    def notify(self,notify_list=[],since=0,time_elapsed=0):
        content = '# PT站点自动签到结果 \n'
        for result in notify_list:
            content = content + '> #### '+ str(result.siteName) +' \n'
            content = content + '> 登录:'
            if result.loginResult == True:
                content = content + '<font color="info">成功</font>'
            else:
                content = content + '<font color="red">失败</font>'
            content = content+'\n'
            content = content + ' 签到:'  
            if result.attendanceResult == True:
                content = content + '<font color="info">成功</font>'
                content = content + '【'
                content = content + result.attendanceResultTxt 
                content = content + '】'
            else:
                content = content + '<font color="red">失败</font>'
            content = content+'\n'
        content = content+'> ### 总用时【 {:.0f}m {:.0f}s】 \n'.format(time_elapsed // 60, time_elapsed % 60)

        data={
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        }
        requests.post(url=self.get_notify_url(),json=data)

