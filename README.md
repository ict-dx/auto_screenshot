# Auto Screenshot

指定した画面領域のスクリーンショットを撮影し、内容の変化を検出して自動で保存するPythonプログラムです。

## 機能
- GUIを使って、スクリーンショットを撮影する領域を選択できます。
- 指定した領域の内容が変化した場合、自動的にスクリーンショットを保存します。
- OpenCVを利用した効率的な画像処理を採用しています。

## 必要要件
- Python 3.7以上
- 必要なPythonライブラリ：
  - `tkinter`（Pythonに標準で含まれています）
  - `pyautogui`
  - `opencv-python`
  - `numpy`

## インストール方法
1. このリポジトリをクローンします：
   ```bash
   git clone https://github.com/username/auto_screenshot.git
   cd auto_screenshot
