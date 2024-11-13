## Overview
api-chrome-link is a Flask-based API service that captures screenshots and HTML source code from web pages using Chrome WebDriver. It provides a secure and efficient way to automate web page capture with features like image compression and size limitations.

## Installation
1. Clone the repository:
```bash
git clone https://github.com/daishir0/api-chrome-link.git
cd api-chrome-link
```

2. Install Chrome browser (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install -y google-chrome-stable
```

3. Install ChromeDriver:
```bash
# First, check your Chrome version
google-chrome --version

# Download the matching ChromeDriver version
wget https://chromedriver.storage.googleapis.com/[VERSION]/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin/
sudo chmod +x /usr/bin/chromedriver
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

5. Setup configuration:
```bash
cp .env.example .env
# Edit .env file with your preferred settings
```

## Usage
1. Start the server:
```bash
python app.py
```

2. API Endpoints:

Screenshot Capture:
```bash
curl -X POST -H "API-KEY: your-api-key" \
     -F "url=https://example.com" \
     http://localhost:6000/get_ss
```

Source Code Capture:
```bash
curl -X POST -H "API-KEY: your-api-key" \
     -F "url=https://example.com" \
     http://localhost:6000/get_source
```

## Notes
- Ensure proper API key configuration in .env file
- Monitor system resources as Chrome instances can be memory-intensive
- Regular cleanup of temporary files is handled automatically
- Consider running behind a reverse proxy in production

## License
This project is licensed under the MIT License - see the LICENSE file for details.

---

# api-chrome-link

## 概要
api-chrome-linkは、Chrome WebDriverを使用してWebページのスクリーンショットとHTMLソースコードを取得するFlaskベースのAPIサービスです。画像圧縮やサイズ制限などの機能を備え、Webページキャプチャを安全かつ効率的に自動化する方法を提供します。

## インストール方法
1. レポジトリをクローンします:
```bash
git clone https://github.com/daishir0/api-chrome-link.git
cd api-chrome-link
```

2. Chrome ブラウザをインストールします (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install -y google-chrome-stable
```

3. ChromeDriverをインストールします:
```bash
# まず、Chromeのバージョンを確認
google-chrome --version

# 対応するバージョンのChromeDriverをダウンロード
wget https://chromedriver.storage.googleapis.com/[VERSION]/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin/
sudo chmod +x /usr/bin/chromedriver
```

4. Python依存パッケージをインストールします:
```bash
pip install -r requirements.txt
```

5. 設定をセットアップします:
```bash
cp .env.example .env
# .envファイルを編集して設定を調整します
```

## 使い方
1. サーバーを起動します:
```bash
python app.py
```

2. APIエンドポイント:

スクリーンショット取得:
```bash
curl -X POST -H "API-KEY: your-api-key" \
     -F "url=https://example.com" \
     http://localhost:6000/get_ss
```

ソースコード取得:
```bash
curl -X POST -H "API-KEY: your-api-key" \
     -F "url=https://example.com" \
     http://localhost:6000/get_source
```

## 注意点
- .envファイルでAPIキーを適切に設定してください
- Chromeインスタンスはメモリを消費するため、システムリソースを監視してください
- 一時ファイルは自動的にクリーンアップされます
- 本番環境では、リバースプロキシの背後での実行を検討してください

## ライセンス
このプロジェクトはMITライセンスの下でライセンスされています。詳細はLICENSEファイルを参照してください。
