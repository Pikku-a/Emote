import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from emote import user_data



GRID_SIZE = 10


class Settings(Gtk.Dialog):
    def __init__(self, update_theme):
        Gtk.Dialog.__init__(
            self,
            title="Hymio Preferences",
            window_position=Gtk.WindowPosition.CENTER,
            resizable=False,
        )

        self.update_theme = update_theme

        header = Gtk.HeaderBar(title="Preferences", show_close_button=True)
        self.set_titlebar(header)

        box = self.get_content_area()

        settings_grid = Gtk.Grid(
            orientation=Gtk.Orientation.VERTICAL,
            margin=GRID_SIZE,
            row_spacing=GRID_SIZE,
        )
        settings_grid.set_row_homogeneous(False)
        settings_grid.set_column_homogeneous(True)

        row = 1

        theme_label = Gtk.Label("Theme")
        theme_label.set_alignment(0, 0.5)
        settings_grid.attach(theme_label, 1, row, 1, 1)

        theme_combo = Gtk.ComboBoxText()
        theme_combo.set_entry_text_column(0)
        theme_combo.connect("changed", self.on_theme_combo_changed)
        for theme in user_data.THEMES:
            theme_combo.append_text(theme)
        theme_combo.set_active(user_data.THEMES.index(user_data.load_theme()))
        settings_grid.attach(theme_combo, 2, row, 1, 1)
        row += 1

        # Add switches for "Enable emoji" and "Enable kaomoji"
        emoji_switch = Gtk.Switch()
        emoji_switch.set_active(user_data.load_emoji_preference())
        emoji_switch.connect("notify::active", self.on_emoji_switch_changed)
        emoji_label = Gtk.Label("Enable emoji")
        emoji_label.set_alignment(0, 0.5)
        settings_grid.attach(emoji_label, 1, row, 1, 1)
        settings_grid.attach(emoji_switch, 2, row, 1, 1)
        row += 1

        kaomoji_switch = Gtk.Switch()
        kaomoji_switch.set_active(user_data.load_kaomoji_preference())
        kaomoji_switch.connect("notify::active", self.on_kaomoji_switch_changed)
        kaomoji_label = Gtk.Label("Enable kaomoji")
        kaomoji_label.set_alignment(0, 0.5)
        settings_grid.attach(kaomoji_label, 1, row, 1, 1)
        settings_grid.attach(kaomoji_switch, 2, row, 1, 1)
        row += 1

        box.pack_start(settings_grid, True, True, GRID_SIZE)

        self.show_all()
        self.present()

    def on_theme_combo_changed(self, combo):
        theme = combo.get_active_text()

        if theme is not None:
            self.update_theme(theme)

    def on_emoji_switch_changed(self, switch, gparam):
        # Call the script to save the preference to the config file
        user_data.save_emoji_preference(switch.get_active())

    def on_kaomoji_switch_changed(self, switch, gparam):
        # Call the script to save the preference to the config file
        user_data.save_kaomoji_preference(switch.get_active())
