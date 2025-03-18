# 卡片生成器插件 (CardPlugin)

![卡片生成器](https://img.shields.io/badge/插件-卡片生成器-brightgreen)
![版本](https://img.shields.io/badge/版本-1.0-blue)
![作者](https://img.shields.io/badge/作者-biubiu-orange)

## 📝 插件介绍

卡片生成器是一个用于生成精美网站分享卡片的插件，支持多种热门网站。用户只需发送简单的命令，即可生成包含网站标题、描述和图标的精美卡片，点击卡片可直接访问对应网站。

### ✨ 主要特点

- 🌐 支持多种热门网站（B站、知乎、微博、淘宝等）
- 🔍 支持模糊匹配，输入部分名称也能匹配到对应网站
- 🎨 自动生成美观的卡片，包含网站标题、描述和图标
- 🛠️ 配置简单，易于扩展

## 🚀 安装方法

1. 将 `card_plugin` 目录复制到 `plugins` 目录下
2. 重启程序，插件将自动加载

## ⚙️ 配置说明

插件配置文件为 `plugins/card_plugin/config.json`，包含以下内容：

```json
{
    "api": {
        "token": "你的API令牌",
        "base_url": "API基础URL",
        "app_id": "你的应用ID"
    },
    "sites": {
        "网站名称1": {
            "url": "网站URL",
            "title": "网站标题",
            "desc": "网站描述",
            "thumb": "网站图标URL",
            "sourceusername": "来源用户名",
            "sourcedisplayname": "来源显示名称"
        },
        "网站名称2": {
            // 网站2的配置
        }
        // 更多网站...
    }
}
```

### API 配置

- `token`: GeWeChat API 的访问令牌
- `base_url`: GeWeChat API 的基础 URL
- `app_id`: GeWeChat 应用 ID

### 网站配置

每个网站可以配置以下字段：

- `url`: 网站的 URL 地址（必填）
- `title`: 卡片显示的标题（可选，默认为"访问{网站名}"）
- `desc`: 卡片显示的描述（可选，默认为"点击访问{网站名}官网"）
- `thumb`: 卡片显示的图标 URL（可选，插件会尝试自动匹配）
- `sourceusername`: 来源用户名（可选）
- `sourcedisplayname`: 来源显示名称（可选，默认为网站名）

## 🎮 使用方法

发送以下命令即可生成对应网站的卡片：

```
card <网站名称>
```

或

```
卡片 <网站名称>
```

### 示例

- `card b站` - 生成哔哩哔哩的卡片
- `卡片 知乎` - 生成知乎的卡片
- `card 淘宝` - 生成淘宝的卡片
- `card bili` - 模糊匹配，生成哔哩哔哩的卡片

## 🔧 添加新网站

要添加新网站，只需在 `config.json` 的 `sites` 部分添加新的配置：

```json
"新网站名称": {
    "url": "https://www.example.com",
    "title": "网站标题",
    "desc": "网站描述",
    "thumb": "https://www.example.com/logo.png",
    "sourceusername": "gh_example",
    "sourcedisplayname": "示例网站"
}
```

也可以使用简化格式，插件会自动补充其他信息：

```json
"新网站名称": "https://www.example.com"
```

## 📋 常见问题

### 卡片无法发送

- 检查 API 配置是否正确
- 确保网络连接正常
- 查看日志中的错误信息

### 卡片显示空白

- 检查网站配置中的 URL 是否正确
- 确保 `thumb` 字段指向有效的图片 URL

## 📄 更新日志

### v1.0 (2025-03-17)

- 初始版本发布
- 支持多种热门网站
- 添加模糊匹配功能
- 自动获取网站图标

## 📝 许可证

本插件基于 MIT 许可证开源。

## 👨‍💻 作者

- biubiu 