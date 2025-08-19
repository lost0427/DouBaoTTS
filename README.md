
<div align="center">

# 🌐 DouBao-TTS

[🇨🇳 中文版](README.md) | [🇺🇸 English](README-en.md)

</div>


这是一个基于 **FastAPI + Edge-TTS** 的 Web 服务，支持输入 **豆包（https://www.doubao.com）分享的对话 URL**，自动提取其中的文本消息并生成 **压缩后的 MP3 音频直链**。  

前端页面支持 **黑白模式切换**，输入 URL 后可获得 MP3 链接并一键复制。

---

## ✨ 功能特性

- 输入 **豆包分享链接**，提取其中的消息内容  
- 使用 **微软 Edge-TTS** 将文本批量转换为音频  
- 自动压缩 MP3（单声道，24kbps）以节省流量  
- 提供 **音频直链**，方便下载或外部调用  
- Web 界面支持 **黑/白主题切换**，操作简洁  

---

## 🚀 使用方法

### 1. 安装依赖
运行批处理脚本：
```bash
install-dbtts.bat
````

### 2. 启动服务

```bash
start-dbtts.bat
```

服务默认运行在：

```
http://[::]:8001
```

---

## 📡 API 接口

### `POST /process`

* **请求参数（JSON）**

  ```json
  {
    "url": "https://www.doubao.com/thread/xxxxxx"
  }
  ```

* **返回参数（成功）**

  ```json
  {
    "code": 1,
    "message": "转换成功",
    "audio_urls": ["/audios/xxxxxx.mp3"]
  }
  ```

* **返回参数（失败）**

  ```json
  {
    "code": -1,
    "message": "错误信息"
  }
  ```

---

## 🖥 前端页面

* 入口地址：`http://[::]:8001/`
* 功能：输入豆包分享链接 → 返回 MP3 → 点击复制直链
* 支持 **黑白主题切换**

---

## 📜 License

本项目基于 **AGPLv3** 协议开源，详情见 [LICENSE](./LICENSE)。
