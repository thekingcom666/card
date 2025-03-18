# encoding:utf-8

"""Card Plugin
A plugin for generating beautiful website cards from JSON config.
"""

# 标准库导入
import os
import json
from typing import Dict, Optional

# 第三方库导入
import requests

# 项目内部导入
from bridge.context import ContextType, Context
from bridge.reply import Reply, ReplyType
from common.log import logger
import plugins
from plugins import Plugin, Event, EventContext, EventAction

@plugins.register(
    name="CardPlugin",
    desire_priority=100,
    desc="生成卡片消息",
    version="1.0",
    author="biubiu",
)
class CardPlugin(Plugin):
    """卡片生成器插件
    
    根据关键词生成精美的网站分享卡片。
    """

    def __init__(self):
        super().__init__()
        try:
            conf = super().load_config()
            if not conf:
                # 配置不存在则写入默认配置
                config_path = os.path.join(os.path.dirname(__file__), "config.json")
                if not os.path.exists(config_path):
                    conf = {
                        "api": {
                            "token": "gewechat_token",
                            "base_url": "gewechat_base_url",
                            "app_id": "gewechat_app_id"
                        },
                        "sites": {
                            "b站": "https://www.bilibili.com",
                            "知乎": "https://www.zhihu.com",
                            "抖音": "https://www.douyin.com",
                            "微博": "https://weibo.com",
                            "小红书": "https://www.xiaohongshu.com"
                        }
                    }
                    with open(config_path, "w", encoding="utf-8") as f:
                        json.dump(conf, f, indent=4, ensure_ascii=False)

            self.api_config = conf.get("api", {})
            self.sites = conf.get("sites", {})
            self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
            logger.info("[CardPlugin] inited")
        except Exception as e:
            logger.warn("[CardPlugin] init failed.")
            raise e

    def _get_site_info(self, keyword: str) -> Optional[Dict]:
        """根据关键词查找网站配置"""
        # 尝试精确匹配
        site_info = self.sites.get(keyword)
        if site_info:
            # 如果是字符串（URL），转换为字典格式
            if isinstance(site_info, str):
                return {
                    "url": site_info,
                    "title": f"访问{keyword}",
                    "desc": f"点击访问{keyword}官网",
                    "thumb": self._get_default_logo(keyword, site_info),
                    "sourceusername": f"gh_{keyword.lower()}",
                    "sourcedisplayname": keyword
                }
            # 如果已经是字典格式，直接返回
            return site_info
            
        # 尝试模糊匹配
        for name, info in self.sites.items():
            if keyword.lower() in name.lower() or name.lower() in keyword.lower():
                logger.info(f"[CardPlugin] Fuzzy match: {keyword} -> {name}")
                if isinstance(info, str):
                    return {
                        "url": info,
                        "title": f"访问{name}",
                        "desc": f"点击访问{name}官网",
                        "thumb": self._get_default_logo(name, info),
                        "sourceusername": f"gh_{name.lower()}",
                        "sourcedisplayname": name
                    }
                return info
                
        # 没有找到匹配的网站
        return None
        
    def _get_default_logo(self, name: str, url: str) -> str:
        """获取网站默认logo"""
        # 常见网站的logo
        logos = {
            "b站": "https://i0.hdslb.com/bfs/archive/1b3cc078268b6c0bcac3391b75d3a3ede90fdf76.png",
            "bilibili": "https://i0.hdslb.com/bfs/archive/1b3cc078268b6c0bcac3391b75d3a3ede90fdf76.png",
            "哔哩哔哩": "https://i0.hdslb.com/bfs/archive/1b3cc078268b6c0bcac3391b75d3a3ede90fdf76.png",
            "知乎": "https://static.zhihu.com/heifetz/assets/apple-touch-icon-152.a53ae37b.png",
            "微博": "https://h5.sinaimg.cn/upload/1059/320/2020/06/16/weibo_logo_2020_white.png",
            "百度": "https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png",
            "github": "https://github.githubassets.com/images/modules/site/social-cards/github-social.png",
            "抖音": "https://lf1-cdn-tos.bytescm.com/obj/static/ies/douyin_web/media/logo-pure.7c95fb62.png",
            "小红书": "https://ci.xiaohongshu.com/5b584f2b-af3e-4c16-a2a4-c64b0d6e2f93",
            "淘宝": "https://img.alicdn.com/imgextra/i1/O1CN01rHzIlP1JlcVnGMDgN_!!6000000001069-2-tps-200-200.png",
            "京东": "https://img10.360buyimg.com/img/jfs/t1/175540/6/19582/4976/60ec3859E0b3aef70/c5d50fa34eb2f8c5.png",
            "网易": "https://static.ws.126.net/f2e/products/post1603/static/images/logo.png",
            "腾讯": "https://mat1.gtimg.com/www/icon/favicon2.ico",
            "qq": "https://qzonestyle.gtimg.cn/qzone/qzact/act/external/tiqq/logo.png",
            "微信": "https://res.wx.qq.com/a/wx_fed/assets/res/NTI4MWU5.ico",
            "豆瓣": "https://img3.doubanio.com/favicon.ico",
            "优酷": "https://img.alicdn.com/tfs/TB1WeJ9Xrj1gK0jSZFuXXcrHpXa-195-195.png",
            "爱奇艺": "https://www.iqiyipic.com/common/fix/site-v4/favicon.ico",
            "今日头条": "https://sf1-cdn-tos.toutiaostatic.com/obj/toutiao-web-fe/tt-fe-next/static/favicon.ico"
        }
        
        # 尝试从名称匹配
        for key, logo in logos.items():
            if key.lower() in name.lower() or name.lower() in key.lower():
                return logo
                
        # 尝试从URL匹配
        domain = url.split("//")[-1].split("/")[0].replace("www.", "")
        for key, logo in logos.items():
            if key.lower() in domain or domain in key.lower():
                return logo
                
        # 默认返回空
        return ""

    def _generate_appmsg(self, site_info: Dict) -> str:
        """生成appmsg XML格式"""
        try:
            # 确保所有必要字段都有值
            title = site_info.get('title', '访问网站')
            desc = site_info.get('desc', '点击访问网站')
            url = site_info.get('url', '')
            thumb = site_info.get('thumb', '')
            sourceusername = site_info.get('sourceusername', '')
            sourcedisplayname = site_info.get('sourcedisplayname', '网站')
            
            # 生成XML
            return f'''<appmsg appid="" sdkver="0">
    <title>{title}</title>
    <des>{desc}</des>
    <action />
    <type>5</type>
    <showtype>0</showtype>
    <soundtype>0</soundtype>
    <mediatagname />
    <messageext />
    <messageaction />
    <content />
    <contentattr>0</contentattr>
    <url>{url}</url>
    <lowurl />
    <dataurl />
    <lowdataurl />
    <appattach>
        <totallen>0</totallen>
        <attachid />
        <emoticonmd5 />
        <fileext />
        <cdnthumburl>{thumb}</cdnthumburl>
        <cdnthumbmd5></cdnthumbmd5>
        <cdnthumblength>0</cdnthumblength>
        <cdnthumbwidth>120</cdnthumbwidth>
        <cdnthumbheight>120</cdnthumbheight>
        <cdnthumbaeskey></cdnthumbaeskey>
        <aeskey></aeskey>
        <encryver>0</encryver>
    </appattach>
    <extinfo />
    <sourceusername>{sourceusername}</sourceusername>
    <sourcedisplayname>{sourcedisplayname}</sourcedisplayname>
    <thumburl>{thumb}</thumburl>
    <md5 />
    <statextstr />
    <mmreadershare>
        <itemshowtype>0</itemshowtype>
    </mmreadershare>
</appmsg>'''
        except Exception as e:
            logger.error(f"[CardPlugin] Error generating appmsg: {e}")
            return ""

    def _send_card(self, to_wxid: str, site_info: Dict) -> bool:
        """发送卡片消息"""
        try:
            # 生成 appmsg
            appmsg = self._generate_appmsg(site_info)
            if not appmsg:
                logger.error("[CardPlugin] Failed to generate appmsg")
                return False
                
            # 发送请求
            url = f"{self.api_config.get('base_url')}/message/postAppMsg"
            headers = {
                "X-GEWE-TOKEN": self.api_config.get('token'),
                "Content-Type": "application/json"
            }
            data = {
                "appId": self.api_config.get('app_id'),
                "toWxid": to_wxid,
                "appmsg": appmsg
            }
            
            logger.info(f"[CardPlugin] Sending card to {to_wxid}, url: {url}")
            logger.debug(f"[CardPlugin] Request data: {data}")
            
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                if result.get("ret") == 200:
                    logger.info(f"[CardPlugin] Card sent successfully to {to_wxid}")
                    return True
                else:
                    logger.error(f"[CardPlugin] Failed to send card: {result.get('msg')}")
            else:
                logger.error(f"[CardPlugin] API request failed: {response.status_code}, {response.text}")
                
        except Exception as e:
            logger.error(f"[CardPlugin] Error sending card: {e}")
            
        return False

    def on_handle_context(self, e_context: EventContext) -> None:
        try:
            context = e_context["context"]
            if context.type != ContextType.TEXT:
                return
            
            content = context.content
            if not content:
                return
                
            if not (content.startswith("card ") or content.startswith("卡片 ")):
                return
                
            # 提取关键词
            keyword = content[5:] if content.startswith("card ") else content[3:]
            keyword = keyword.strip()
            
            if not keyword:
                reply = Reply(ReplyType.TEXT, "请指定要生成卡片的网站，例如：card b站")
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS
                return
                
            # 查找网站配置
            site_info = self._get_site_info(keyword)
            if not site_info:
                reply = Reply(ReplyType.TEXT, f"未找到网站 {keyword} 的配置")
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS
                return
                
            # 获取接收人ID
            to_wxid = context.kwargs.get("receiver")
            if not to_wxid:
                logger.error("[CardPlugin] No receiver in context")
                reply = Reply(ReplyType.TEXT, "无法获取接收人信息")
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS
                return
                
            # 生成并发送卡片
            if self._send_card(to_wxid, site_info):
                e_context.action = EventAction.BREAK_PASS
            else:
                reply = Reply(ReplyType.TEXT, "发送卡片失败")
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS
                
        except Exception as e:
            logger.error(f"[CardPlugin] Error handling message: {e}")
            reply = Reply(ReplyType.TEXT, f"处理消息失败：{e}")
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS

    def get_help_text(self, **kwargs) -> str:
        """获取帮助信息"""
        # 获取配置中的网站列表
        available_sites = "、".join(self.sites.keys())
        
        # 构建帮助信息
        help_text = f"""【卡片生成器】

✨ 功能说明：
  生成精美的网站分享卡片，点击可直接访问对应网站。

📝 使用方法：
  card <网站名称>  或  卡片 <网站名称>

🌐 支持网站：
  {available_sites}

📱 示例：
  card b站
  卡片 知乎
  card 淘宝

💡 提示：
  支持模糊匹配，例如输入"bili"也可以匹配到"b站"。
"""
        return help_text 