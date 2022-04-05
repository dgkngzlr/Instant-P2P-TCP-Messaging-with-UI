from ast import Call
import dearpygui.dearpygui as dpg
from callbacks import Callback

dpg.create_context()
callbck_object= Callback()

# Main window layout
with dpg.window(tag="main_window"):

    # Menu bar items are here
    with dpg.menu_bar():
        dpg.add_menu_item(label="About", callback=callbck_object.about_callback)

    dpg.add_text("Message History :")

    # Place history_text, connect_button, radio button and information
    with dpg.group(horizontal=True):

        # History text is placed in horizontal manner respect to other items
        history_text = dpg.add_input_text(tag="history_text", height=400, multiline=True, readonly=True)  # Callback

        # connect_button, radio button and information are placed vertical manner
        with dpg.group(horizontal=False):
            connect_button = dpg.add_button(tag="connect_button", label="Connect", width=-1,
                                            callback=callbck_object.connect_button_callback)
            # New line
            dpg.add_text("")

            dpg.add_radio_button(tag="radio_button", items=["Encrypted", "Non-Encrypted"], default_value="Encrypted",
                                 callback=callbck_object.radio_button_callback)
            dpg.add_text("")
            dpg.add_text("")

            # Host and remote information
            dpg.add_text("Information :")
            dpg.add_text(tag="host_info")
            dpg.add_text("")
            dpg.add_text(tag="remote_info")

    dpg.add_text("")

    # Bottom part of gui
    with dpg.group(horizontal=True):
        message_text = dpg.add_input_text(tag="message_text", hint="Enter your message", on_enter=True, callback=callbck_object.send_button_callback )
        send_button = dpg.add_button(label="Send", width=-1, callback=callbck_object.send_button_callback)  # Callback

# About window generation
with dpg.window(label="About", modal=True, show=False, id="modal_about", width=380):
    dpg.add_text("Version : v0.1")
    dpg.add_text("Description : This application provides \nencrypted instant messaging between P2P")
    dpg.add_separator()

    with dpg.table(header_row=False, resizable=True):
        dpg.add_table_column(width=10, width_stretch=True)
        dpg.add_table_column(width=100, width_stretch=True)
        dpg.add_table_column(width=10, width_stretch=True)
        with dpg.table_row():
            dpg.add_text(default_value="")
            dpg.add_button(label="Close", width=100, callback=lambda: dpg.configure_item("modal_about", show=False))
            dpg.add_text(default_value="")

# General theme settings
with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6, category=dpg.mvThemeCat_Core)

with dpg.font_registry():
    default_font = dpg.add_font("./fonts/UbuntuMono-Regular.ttf", 15)

dpg.bind_theme(global_theme)
dpg.bind_font(default_font)

if __name__ == "__main__":
    dpg.set_primary_window("main_window", True)
    dpg.create_viewport(title="My App", width=800, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
