import datetime
import subprocess
import time
import os

# 获取当前用户名和时间信息
current_user = os.getlogin()
formatted_time = int(datetime.datetime.now().strftime("%H"))

print('当前时间：', formatted_time ,'时')
print('当前用户：', current_user)

# 定义主题切换时间
light_theme_time = 7 <= formatted_time < 18  #浅色主题切换时间，早上7点到下午18点切换到浅色主题，其余时间都切换到深色主题（可自行调整）


# 根据当前用户名构建主题文件路径（注意，大小写要严格）
# windows 的默认主题路径一般在：C:\WINDOWS\resources\Themes
# 用户自定义的主题路径一般在：C:\Users\用户名\AppData\Local\Microsoft\Windows\Themes

light_theme_path = 'C:\\WINDOWS\\resources\\Themes\\aero.theme'
dark_theme_path  = 'C:\\WINDOWS\\resources\\Themes\\dark.theme'

# light_theme_path = f'C:\\Users\\{current_user}\\AppData\\Local\\Microsoft\\Windows\\Themes\\自定义-浅色.theme'
# dark_theme_path  = f'C:\\Users\\{current_user}\\AppData\\Local\\Microsoft\\Windows\\Themes\\自定义-深色.theme'


def switch_theme():

    #打开设置面板
    subprocess.run('start ms-settings:', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # 切换主题
    global command

    if light_theme_time:    # 早上7点到下午18点切换到浅色主题
        command = f'start "" "{light_theme_path}"'
        print('切换到浅色主题')
    else:                           # 其余时间切换到深色主题
        command = f'start "" "{dark_theme_path}"'
        print('切换到深色主题')

    subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


# 切换主题
# switch_theme()

# 验证主题是否更改成功
theme_changed = False
while not theme_changed:
    
    formatted_time = int(datetime.datetime.now().strftime("%H"))  # 更新当前时间段

    # 根据当前时间段进行主题检测
    expected_theme = light_theme_path if (light_theme_time) else dark_theme_path

    result = subprocess.run('reg query "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes" /v CurrentTheme',
                            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    current_theme = result.stdout.split()[-1]  # 获取当前主题路径

    if current_theme == expected_theme:
        print("主题更改成功.")
        theme_changed = True
    else:
        print(f"当前时间为 {formatted_time} 时，主题未更改成功，正在重试...")
        switch_theme()  # 切换主题


# 检测设置面板是否已经关闭
i = 0
while i <10:
    
    # 检测并关闭 设置面板
    result = subprocess.run('tasklist /fi "IMAGENAME eq SystemSettings.exe"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output = result.stdout.lower()
    if "systemsettings.exe" in output:
        print("检测到设置面板，将其关闭...")
        subprocess.run('taskkill /f /im "SystemSettings.exe"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    else:
        print('未检测到设置面板，再次循环检测')
        print('当你看到这个弹窗，而为这个弹窗遮挡视线而感到烦恼的时候，请检查是否有按照我写的教程方法里提到的要使用`pythonw.exe`文件而非`python`文件来执行脚本')

    i += 1
    time.sleep(1)

os._exit(0)
