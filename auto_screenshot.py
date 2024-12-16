import tkinter as tk
import pyautogui
import cv2
import numpy as np
import time
import os
from datetime import datetime

class SelectionApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-alpha", 0.3)  # 半透明ウィンドウ
        self.root.attributes("-fullscreen", True)  # フルスクリーン化
        
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="gray")
        self.canvas.pack(fill="both", expand=True)
        
        self.start_x = None
        self.start_y = None
        self.rect = None

        # マウスイベントバインド
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.selection = None  # 選択領域(x, y, width, height)を保持する

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        # 新たな矩形描画
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, 
                                                 self.start_x, self.start_y,
                                                 outline='red', width=2)

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        end_x, end_y = (event.x, event.y)
        # 左上(x1, y1)、右下(x2, y2)を取得し、width/heightを算出
        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)

        width = x2 - x1
        height = y2 - y1
        self.selection = (x1, y1, width, height)

        # 選択完了後ウィンドウを閉じる
        self.root.destroy()

    def run(self):
        self.root.mainloop()
        return self.selection

def image_change_rate(img1, img2):
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    mdframe = cv2.absdiff(gray1, gray2)
    thresh = cv2.threshold(mdframe, 10, 255, cv2.THRESH_BINARY)[1]

    image_size = thresh.size
    white_pixels = cv2.countNonZero(thresh)
    white_area_ratio = white_pixels / image_size
    return white_area_ratio

# -------------------------------------
# メイン処理
# -------------------------------------
save_dir = "C:\\Users\\ueda\\Documents\\screenshot"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

app = SelectionApp()
region = app.run()
if region is None:
    print("No region selected. Exiting...")
    exit()

print("Selected region:", region)

# 領域指定後に1回スクリーンショットを撮って保存
pil_img = pyautogui.screenshot(region=region)
current_img_np = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

# ファイル保存
now = datetime.now().strftime("%Y%m%d_%H%M%S")
filepath = os.path.join(save_dir, f"screenshot_{now}.png")
cv2.imwrite(filepath, current_img_np)
print(f"Initial screenshot saved: {filepath}")

change_threshold = 0.1  # 変化率のしきい値は0.1など適宜調整

prev_img_np = None

while True:
    pil_img = pyautogui.screenshot(region=region)
    current_img_np = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    
    if prev_img_np is not None:
        change_rate = image_change_rate(prev_img_np, current_img_np)
        print("change_rate:", change_rate)
        
        if change_rate > change_threshold:
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(save_dir, f"screenshot_{now}.png")
            # cv2で保存
            cv2.imwrite(filepath, current_img_np)
            print(f"Slide changed! Saved screenshot: {filepath}")
            
            # ここでprev_img_npを更新
            prev_img_np = current_img_np
    else:
        prev_img_np = current_img_np

    time.sleep(5)
