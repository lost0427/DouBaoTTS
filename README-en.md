
<div align="center">

# 🌐 DouBao-TTS

[🇨🇳 中文版](README.md) | [🇺🇸 English](README-en.md)

</div>


This is a web service built with **FastAPI + Edge-TTS**, designed to support input of **conversation URLs shared by Doubao (https://www.doubao.com)**. It automatically extracts the text messages from these URLs and generates **compressed MP3 audio direct links**.

The frontend interface includes a **black-and-white theme toggle**, allowing users to switch between themes after entering a URL, after which they can obtain the MP3 link and copy it with a single click.

---

## ✨ Key Features

- Input **Doubao share links** to extract message content  
- Use **Microsoft Edge-TTS** to convert text into audio in batch  
- Automatically compress MP3 files (mono, 24 kbps) to save bandwidth  
- Provide **direct audio links** for easy downloading or external access  
- The web interface supports **dark/light theme switching**, offering a clean and intuitive user experience  

---

## 🚀 How to Use

### 1. Install Dependencies
Run the batch script:
```bash
install-dbtts.bat
```

### 2. Start the Service
```bash
start-dbtts.bat
```

By default, the service will run on:
```
http://[::]:8001
```

---

## 📡 API Endpoints

### `POST /process`

* **Request Parameters (JSON)**

  ```json
  {
    "url": "https://www.doubao.com/thread/xxxxxx"
  }
  ```

* **Response Parameters (Success)**

  ```json
  {
    "code": 1,
    "message": "Conversion successful",
    "audio_urls": ["/audios/xxxxxx.mp3"]
  }
  ```

* **Response Parameters (Failure)**

  ```json
  {
    "code": -1,
    "message": "Error message"
  }
  ```

---

## 🖥 Frontend Interface

* Entry point: `http://[::]:8001/`  
* Functionality: Enter a Doubao share link → Receive MP3 file → Click to copy the direct link  
* Supports **black-and-white theme switching**

---

## 📜 License

This project is open-sourced under the **AGPLv3** license. For details, please refer to [LICENSE](./LICENSE).