@echo off
echo Installing required Python packages...

pip install pyautogui
pip install imgui[glfw]
pip install glfw
pip install keyboard
pip install PyOpenGL

echo All packages installed.
pause
