import pyautogui
import imgui
from imgui.integrations.glfw import GlfwRenderer
import glfw
import OpenGL.GL as gl
import keyboard
import time

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05

class ColorBotApp:
    def __init__(self):
        self.target_color = [75, 219, 106]
        self.keybind = 't'
        self.keybind_input = ['t']
        self.mode = 'toggle'  # or 'hold'
        self.bot_enabled = False
        self.last_check = 0
        self.last_key_state = False
        self.scan_delay = 50  # delay in ms, default 50ms

    def init_window(self):
        if not glfw.init():
            raise Exception("GLFW init failed")

        window = glfw.create_window(400, 300, "ColorBot by Jaya <$", None, None)
        if not window:
            glfw.terminate()
            raise Exception("Failed to create window")

        glfw.make_context_current(window)
        gl.glClearColor(0.1, 0.1, 0.1, 1)
        imgui.create_context()
        self.impl = GlfwRenderer(window)
        return window

    def check_color(self):
        if not self.bot_enabled:
            return
        now = time.time()
        # If delay > 0, check if enough time has passed
        if self.scan_delay > 0 and (now - self.last_check) * 1000 < self.scan_delay:
            return
        self.last_check = now

        screenshot = pyautogui.screenshot()
        target = tuple(self.target_color)
        for x in range(0, screenshot.width, 5):
            for y in range(0, screenshot.height, 5):
                if screenshot.getpixel((x, y)) == target:
                    pyautogui.click()  # Click at current mouse position
                    time.sleep(0.1)
                    return

    def handle_keybind(self):
        key = self.keybind.lower()
        pressed = keyboard.is_pressed(key)

        if self.mode == 'hold':
            self.bot_enabled = pressed
        else:
            if pressed and not self.last_key_state:
                self.bot_enabled = not self.bot_enabled
            self.last_key_state = pressed

    def render_ui(self):
        imgui.begin("ColorBot by Jaya <$", True)

        imgui.text(f"Status: {'Running' if self.bot_enabled else 'Stopped'}")
        if self.bot_enabled:
            imgui.text_colored("●", 0, 1, 0, 1)
        else:
            imgui.text_colored("●", 1, 0, 0, 1)

        color_float = [c / 255.0 for c in self.target_color]
        changed, new_color = imgui.color_edit3("Target Color", *color_float)
        if changed:
            self.target_color = [int(c * 255) for c in new_color]

        changed, new_key = imgui.input_text("Keybind", self.keybind_input[0], 4)
        if changed and new_key:
            self.keybind_input[0] = new_key
            self.keybind = new_key.lower()

        if imgui.radio_button("Toggle Mode", self.mode == 'toggle'):
            self.mode = 'toggle'
        imgui.same_line()
        if imgui.radio_button("Hold Mode", self.mode == 'hold'):
            self.mode = 'hold'

        changed, val = imgui.slider_int("Scan Delay (ms)", self.scan_delay, 0, 100)
        if changed:
            self.scan_delay = val

        if imgui.button("Quit"):
            glfw.set_window_should_close(glfw.get_current_context(), True)

        imgui.end()

    def run(self):
        window = self.init_window()
        while not glfw.window_should_close(window):
            glfw.poll_events()
            self.impl.process_inputs()
            imgui.new_frame()

            self.handle_keybind()
            self.check_color()
            self.render_ui()

            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            imgui.render()
            self.impl.render(imgui.get_draw_data())
            glfw.swap_buffers(window)

        self.impl.shutdown()
        glfw.terminate()

if __name__ == "__main__":
    ColorBotApp().run()
