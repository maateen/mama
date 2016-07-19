import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk
from os.path import expanduser
import os

class SetupWindow():
    def __init__(self,button_back, button_cancel):
        # class variables
        self.config_file = expanduser('~') + '/.config/mama/mama.conf'
        self.locale = 'en-US'
        self.audio_chunk = 1024
        self.audio_channels = 2
        self.audio_rate = 8000  # sample rate
        self.recording_time = 3  # in second
        self.client_id = ''
        self.api_key = ''
        self.speaker = 'Mama (Male)'

        # looking for the configuration file
        self.__loadconfig()

        label0 = Gtk.Label('Set Your Locale')
        label0.set_justify(Gtk.Justification.LEFT)
        label0.set_halign(Gtk.Align.START)
        label0.set_hexpand(True)
        label1 = Gtk.Label('Set Audio Chunk')
        label1.set_justify(Gtk.Justification.LEFT)
        label1.set_halign(Gtk.Align.START)
        label2 = Gtk.Label('Set Number of Channels')
        label2.set_justify(Gtk.Justification.LEFT)
        label2.set_halign(Gtk.Align.START)
        label3 = Gtk.Label('Set Sampling Rate')
        label3.set_justify(Gtk.Justification.LEFT)
        label3.set_halign(Gtk.Align.START)
        label4 = Gtk.Label('Set the Recording Time (in second)')
        label4.set_justify(Gtk.Justification.LEFT)
        label4.set_halign(Gtk.Align.START)
        label5 = Gtk.Label('Set Microsoft Azure Client ID')
        label5.set_justify(Gtk.Justification.LEFT)
        label5.set_halign(Gtk.Align.START)
        label6 = Gtk.Label('Set Microsoft Bing Speech Api Key')
        label6.set_justify(Gtk.Justification.LEFT)
        label6.set_halign(Gtk.Align.START)
        label7 = Gtk.Label('Set Speaker (who will talk to you?)')
        label7.set_justify(Gtk.Justification.LEFT)
        label7.set_halign(Gtk.Align.START)
        label7.set_hexpand(True)

        combo = self.__get_combobox()

        self.entry1 = Gtk.Entry()
        self.entry1.set_text(str(self.audio_chunk))
        self.entry1.set_tooltip_text('Set the audio chunk')

        self.entry2 = Gtk.Entry()
        self.entry2.set_text(str(self.audio_channels))
        self.entry2.set_tooltip_text('Set audio channels')

        rate_combo = self.__get_rate_combobox()

        self.scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 1, 10,
                                              1)
        self.scale.set_value(self.recording_time)
        self.scale.connect("value-changed", self.scale_moved)
        self.scale.set_tooltip_text('Change the recording time')

        self.entry5 = Gtk.Entry()
        self.entry5.set_text(self.client_id)
        self.entry5.set_tooltip_text('Set Microsoft Azure Client ID')

        self.entry6 = Gtk.Entry()
        self.entry6.set_text(self.api_key)
        self.entry6.set_tooltip_text('Set Microsoft Bing Speech Api Key')

        speaker_combo = self.__get_speaker_combobox()

        button_back.connect("clicked",self.on_clicked)

        # an invisble widget to fill the window
        ll = Gtk.Label()
        ll.set_vexpand(True)

        self.grid = Gtk.Grid()
        self.grid.set_border_width(10)
        self.grid.set_row_spacing(15)
        self.grid.set_vexpand(True)
        self.grid.set_hexpand(True)
        self.grid.set_column_spacing(2)
        self.grid.set_column_homogeneous(False)
        self.grid.attach(label0, 0, 0, 14, 1)
        self.grid.attach(combo, 14, 0, 1, 1)
        self.grid.attach(label1, 0, 1, 14, 1)
        self.grid.attach(self.entry1, 11, 1, 4, 1)
        self.grid.attach(label2, 0, 2, 14, 1)
        self.grid.attach(self.entry2, 11, 2, 4, 1)
        self.grid.attach(label3, 0, 3, 11, 1)
        self.grid.attach(rate_combo, 14, 3, 1, 1)
        self.grid.attach(label4, 0, 4, 11, 1)
        self.grid.attach(self.scale, 11, 4, 4, 1)
        self.grid.attach(label5, 0, 5, 11, 1)
        self.grid.attach(self.entry5, 11, 5, 4, 1)
        self.grid.attach(label6, 0, 6, 11, 1)
        self.grid.attach(self.entry6, 11, 6, 4, 1)
        self.grid.attach(label7, 0, 7, 14, 1)
        self.grid.attach(speaker_combo, 14, 7, 1, 1)
        self.grid.attach(ll, 0, 8, 15, 1)
        self.grid.attach(button_cancel, 13, 9, 1, 1)
        self.grid.attach(button_back, 14, 9, 1, 1)

    # load the config_file
    def __loadconfig(self):
        # if a config_file file is available
        if os.path.exists(self.config_file):
            try:
                # here we load
                with open(self.config_file, "r") as f:
                    for line in f.readlines():
                        line = line.strip('\n')
                        #get the field
                        field = line.split('=')
                        if len(field) >= 2:
                            if field[0] == 'locale':
                                self.locale = field[1].replace('"', '')
                            elif field[0] == 'audio_chunk':
                                self.audio_chunk = int(field[1])
                            elif field[0] == 'audio_channels':
                                self.audio_channels = int(field[1])
                            elif field[0] == 'audio_rate':
                                self.audio_rate = int(field[1])
                            elif field[0] == 'recording_time':
                                self.recording_time = int(field[1])
                            elif field[0] == 'client_id':
                                self.client_id = field[1].replace('"','')
                            elif field[0] == 'api_key':
                                self.api_key = field[1].replace('"', '')
                            elif field[0] == 'speaker':
                                self.speaker = field[1].replace('"', '')

            except Exception:
                print("Config file", self.config_file)
                print("missing...")

    # record the config_file
    def __recordconfig(self):
        try:
            with open(self.config_file, "w") as f:
                f.write('locale="' + self.locale + '"\n')
                f.write(
                    'audio_chunk=' + self.entry1.get_text().strip(' ') + '\n')
                f.write('audio_channels=' + self.entry2.get_text().strip(
                    ' ') + '\n')
                f.write('audio_rate=' + str(self.audio_rate) + '\n')
                f.write('recording_time=' + str(self.recording_time).strip(
                    ' ') + '\n')
                f.write(
                    'client_id="' + self.entry5.get_text().strip(' ') + '"\n')
                f.write('api_key="' + self.entry6.get_text().strip(' ') + '"\n')
                f.write('speaker="' + self.speaker + '"\n')
                f.close()
        except Exception:
            print("Config file", self.config_file)
            print("Unable to write")

    # get the grid
    def getGrid(self):
        return self.grid

    def scale_moved(self,event):
        self.recording_time = int(self.scale.get_value())
        self.__recordconfig()

    def on_clicked(self,button):
        self.__recordconfig()

    # return a combobox to add to the toolbar
    def __get_combobox(self):
        """
        @description: get the combobox of the toolbar

        @return: a Gtk.Combobox
        """
        # the data in the model, of type string
        listmodel = Gtk.ListStore(str)
        # append the data in the model
        selected = 4
        i = 0
        self.language_list = ['en-AU', 'en-CA', 'en-GB', 'en-IN', 'en-US']
        for language_name in self.language_list:
            listmodel.append([language_name])
            if language_name == self.locale:
                selected = i
            i += 1

        # a combobox to see the data stored in the model
        combobox = Gtk.ComboBox(model=listmodel)
        combobox.set_tooltip_text("What format to choose?")

        # a cellrenderer to render the text
        cell = Gtk.CellRendererText()

        # pack the cell into the beginning of the combobox, allocating
        # no more space than needed
        combobox.pack_start(cell, False)
        # associate a property ("text") of the cellrenderer (cell) to a column (column 0)
        # in the model used by the combobox
        combobox.add_attribute(cell, "text", 0)

        # the first row is the active one by default at the beginning
        combobox.set_active(selected)

        # connect the signal emitted when a row is selected to the callback function
        combobox.connect("changed", self.on_combochanged)
        return combobox

    def on_combochanged(self, combo):
        self.locale = str(self.language_list[combo.get_active()])
        self.__recordconfig()

    # return a sample rate combobox to add to the toolbar
    def __get_rate_combobox(self):
        """
        @description: get the sample rate combobox of the toolbar

        @return: a Gtk.Combobox
        """
        # the data in the model, of type string
        listmodel = Gtk.ListStore(int)
        # append the data in the model
        selected = 0
        i = 0
        self.rate_list = [8000, 16000]
        for rate_name in self.rate_list:
            listmodel.append([rate_name])
            if rate_name == self.audio_rate:
                selected = i
            i += 1

        # a combobox to see the data stored in the model
        rate_combobox = Gtk.ComboBox(model=listmodel)
        rate_combobox.set_tooltip_text("Set Sampling Rate")

        # a cellrenderer to render the text
        rate_cell = Gtk.CellRendererText()

        # pack the cell into the beginning of the combobox, allocating
        # no more space than needed
        rate_combobox.pack_start(rate_cell, False)
        # associate a property ("text") of the cellrenderer (cell) to a column (column 0)
        # in the model used by the combobox
        rate_combobox.add_attribute(rate_cell, "text", 0)

        # the first row is the active one by default at the beginning
        rate_combobox.set_active(selected)

        # connect the signal emitted when a row is selected to the callback function
        rate_combobox.connect("changed", self.on_rate_combochanged)
        return rate_combobox

    def on_rate_combochanged(self, combo):
        self.audio_rate = self.rate_list[combo.get_active()]
        print(self.audio_rate)
        print(type(self.audio_rate))
        self.__recordconfig()

    # return a speaker combobox to add to the toolbar
    def __get_speaker_combobox(self):
        """
        @description: get the speaker combobox of the toolbar

        @return: a Gtk.Combobox
        """
        # the data in the model, of type string
        listmodel = Gtk.ListStore(str)
        # append the data in the model
        selected = 0
        i = 0
        self.speaker_list = ['Mama (Male)', 'His Wife (Female)']
        for speaker_name in self.speaker_list:
            listmodel.append([speaker_name])
            if speaker_name == self.speaker:
                selected = i
            i += 1

        # a combobox to see the data stored in the model
        speaker_combobox = Gtk.ComboBox(model=listmodel)
        speaker_combobox.set_tooltip_text("Whose speaker to choose?")

        # a cellrenderer to render the text
        speaker_cell = Gtk.CellRendererText()

        # pack the cell into the beginning of the combobox, allocating
        # no more space than needed
        speaker_combobox.pack_start(speaker_cell, False)
        # associate a property ("text") of the cellrenderer (cell) to a column (column 0)
        # in the model used by the combobox
        speaker_combobox.add_attribute(speaker_cell, "text", 0)

        # the first row is the active one by default at the beginning
        speaker_combobox.set_active(selected)

        # connect the signal emitted when a row is selected to the callback function
        speaker_combobox.connect("changed", self.on_speaker_combochanged)
        return speaker_combobox

    def on_speaker_combochanged(self, combo):
        self.speaker = str(self.speaker_list[combo.get_active()])
        self.__recordconfig()
