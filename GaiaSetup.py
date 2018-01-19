import wx
import wx.grid
import random
from Gaia import Map

demo_map_path = "images/MapDemo.png"
standard_map_path = "images/StandardMap.png"
default_map_path = "images/Gaia_map.png"
background_path = "images/Tech_bg.png"
image_path = "images/"
image_format = ".png"

TEC = ['TECore', 'TECcre', 'TECknw', 'TECpow', 'TECqic', 'TECpia', 'TECgai', 'TECtyp', 'TECvps']
ADV = ['ADVore', 'ADVknw', 'ADVqic', 'ADVgai', 'ADVtyp', 'ADVstp', 'ADVlab', 'ADVminV', 'ADVminB', 'ADVtrsV',
       'ADVtrsB', 'ADVsecV', 'ADVsecO', 'ADVfedV', 'ADVfedP']
BOO = ['BOOnav', 'BOOter', 'BOOmin', 'BOOtrs', 'BOOlab', 'BOOpia', 'BOOgai', 'BOOqic', 'BOOpwt', 'BOOknw']
RND = ['RNDter', 'RNDfed', 'RNDstp', 'RNDmin', 'RNDtrs3', 'RNDtrs4', 'RNDpia', 'RNDpia', 'RNDgai3', 'RNDgai4']
FIN = ['FINbld', 'FINfed', 'FINgai', 'FINsec', 'FINsat', 'FINtyp']
FED = ['FEDknw', 'FEDore', 'FEDcre', 'FEDqic', 'FEDpwt']

list_of_pieces = [FED[:], ADV[:], TEC[:], TEC[:], BOO[:], RND[:], FIN[:]]
num_pics = [1, 6, 6, 3, 7, 6, 2]
color_list = [(160, 101, 85),(110, 131, 162),(88, 162, 51),(171, 11, 119),(247, 165, 1),(0, 156, 223),(159, 165, 176)]

class MainFrame(wx.Frame):
    def __init__(self, parent=None):
        super(MainFrame, self).__init__(parent, title="Gaia Setup", size=(1200, 850))
        self.default_font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.make_menu()
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.SetFont(self.default_font)

        self.default_num_players = 2

        #icon

        self.panel = wx.Panel(self)
        self.notebook = NotebookStructure(self, self.panel)
        self.map_tab = self.notebook.get_map_tab()
        self.setup_tab = self.notebook.get_setup_tab()

        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(self.notebook, 1, wx.ALL | wx.EXPAND, 5)
        self.panel.SetSizer(vsizer)
        self.Centre()
        self.Show()

    def make_menu(self):
        pass

    def on_close(self, event):
        self.Destroy()

    def get_default_num_players(self):
        return self.default_num_players


class NotebookStructure(wx.Notebook):
    def __init__(self, parent, panel):
        wx.Notebook.__init__(self, panel, id=wx.ID_ANY, style=wx.BK_DEFAULT)
        self.parent = parent
        self.panel = panel
        self.map_tab = MapTab(self)
        self.setup_tab = SetupTab(self)

        self.AddPage(self.map_tab, "Map")
        self.AddPage(self.setup_tab, "Setup")

    def get_map_tab(self):
        return self.map_tab

    def get_setup_tab(self):
        return self.setup_tab

    def get_default_num_players(self):
        return self.parent.get_default_num_players()

class MapTab(wx.Panel):
    def __init__(self, parent):
        super(MapTab, self).__init__(parent=parent, id=wx.ID_ANY)
        self.parent = parent
        self.png = None
        self.default_num_players = self.parent.get_default_num_players()
        self.PhotoMaxSize = 800

        img = wx.Image(standard_map_path, wx.BITMAP_TYPE_ANY)
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H

        img = img.Scale(NewW, NewH)
        self.imageMap = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img))

        self.hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.hsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.vsizer2 = wx.BoxSizer(wx.VERTICAL)

        players_info_text = wx.StaticText(self, -1, "Number of players")
        self.players_number = wx.TextCtrl(self, value=str(self.default_num_players))
        btn_make_map = wx.Button(self, wx.ID_OK, label="Generate map", size=(120, 40))
        self.Bind(wx.EVT_BUTTON, self.on_make_map, btn_make_map)

        self.vsizer.Add(players_info_text, 1)
        self.vsizer.Add(self.players_number, 1)

        self.hsizer.Add(self.vsizer, 1, wx.EXPAND | wx.ALL, 20)
        self.hsizer.Add(btn_make_map, 1, wx.EXPAND | wx.ALL, 20)
        self.hsizer2.Add(self.imageMap, 0, wx.ALL, 5)
        self.vsizer2.Add(self.hsizer, 0)    # setup
        self.vsizer2.Add(self.hsizer2, 0, wx.EXPAND)

        self.SetSizer(self.vsizer2)

    def on_make_map(self, event):
        n_players = int(self.players_number.GetValue())
        self.map = Map(n_players)

        # TODO: optimize!!!!!

        self.map.save_image_map()
        self.set_map(default_map_path)

    def set_map(self, image_path):
        img = wx.Image(image_path, wx.BITMAP_TYPE_ANY)
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(NewW, NewH)
        self.imageMap.SetBitmap(wx.Bitmap(img))


class SetupTab(wx.Panel):
    def __init__(self, parent):
        super(SetupTab, self).__init__(parent=parent, id=wx.ID_ANY)
        self.parent = parent
        self.default_num_players = self.parent.get_default_num_players()
        self.resize_factor = 0.8

        self.hsizer_input = wx.BoxSizer(wx.HORIZONTAL)
        self.hsizer_output = wx.BoxSizer(wx.HORIZONTAL)
        self.vsizer_input = wx.BoxSizer(wx.VERTICAL)
        self.vsizer_overall = wx.BoxSizer(wx.VERTICAL)

        players_info_text = wx.StaticText(self, -1, "Number of players")
        self.players_number = wx.TextCtrl(self, value=str(self.default_num_players))
        btn_randomize = wx.Button(self, wx.ID_OK, label="Randomize setup", size=(140, 40))
        self.Bind(wx.EVT_BUTTON, self.on_randomize, btn_randomize)

        self.vsizer_input.Add(players_info_text, 1)
        self.vsizer_input.Add(self.players_number, 1)

        self.hsizer_input.Add(self.vsizer_input, 1, wx.EXPAND | wx.ALL, 20)
        self.hsizer_input.Add(btn_randomize, 1, wx.EXPAND | wx.ALL, 20)
        self.vsizer_overall.Add(self.hsizer_input, 0)    # setup
        vsizer_output = wx.BoxSizer(wx.VERTICAL)

        self.hsizer_tech_tracks = wx.BoxSizer(wx.HORIZONTAL)
        self.hsizer_extra_tech = wx.BoxSizer(wx.HORIZONTAL)
        self.hsizer_round_score = wx.BoxSizer(wx.HORIZONTAL)
        self.hsizer_boosters = wx.BoxSizer(wx.HORIZONTAL)
        self.htracks = [self.hsizer_tech_tracks, self.hsizer_extra_tech, self.hsizer_round_score, self.hsizer_boosters]

        background = wx.Image(background_path, wx.BITMAP_TYPE_ANY)
        background_img = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(background))

        for i in range(6):
            panel = wx.Panel(self)
            panel.BackgroundColour = color_list[i]

            if i == 0: # Brown
                hsizer = wx.BoxSizer(wx.HORIZONTAL)
                brown_vsizer1 = wx.BoxSizer(wx.VERTICAL)
                brown_vsizer2 = wx.BoxSizer(wx.VERTICAL)

                path = image_path + list_of_pieces[0][0] + image_format
                brown_fed = wx.Image(path, wx.BITMAP_TYPE_ANY)
                W = brown_fed.GetWidth()
                H = brown_fed.GetHeight()
                local_factor = 0.8
                brown_fed = brown_fed.Scale(int(W*self.resize_factor*local_factor),
                                            int(H*self.resize_factor*local_factor))
                brown_fed_image = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(brown_fed))
                brown_vsizer1.Add(brown_fed_image, 1, wx.ALL)

                path1 = image_path + list_of_pieces[1][i] + image_format
                img1 = wx.Image(path1, wx.BITMAP_TYPE_ANY)
                W = img1.GetWidth()
                H = img1.GetHeight()
                img1 = img1.Scale(int(W * self.resize_factor), int(H * self.resize_factor))
                img1_bm = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img1))
                path2 = image_path + list_of_pieces[2][i] + image_format
                img2 = wx.Image(path2, wx.BITMAP_TYPE_ANY)
                W = img2.GetWidth()
                H = img2.GetHeight()
                img2 = img2.Scale(int(W * self.resize_factor), int(H * self.resize_factor))
                img2_bm = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img2))

                brown_vsizer2.Add(img1_bm, 1, wx.ALL, 5)
                brown_vsizer2.Add(img2_bm, 1, wx.ALL, 5)

                hsizer.Add(brown_vsizer1, 1, wx.ALL)
                hsizer.Add(brown_vsizer2, 1, wx.ALL)

                self.hsizer_tech_tracks.Add(hsizer, 1, wx.EXPAND | wx.ALL)

                #panel.SetSizer(hsizer)
                #self.hsizer_tech_tracks.Add(panel, 1, wx.EXPAND | wx.ALL)
            else:
                vsizer = wx.BoxSizer(wx.VERTICAL)

                path1 = image_path + list_of_pieces[1][i] + image_format
                img1 = wx.Image(path1, wx.BITMAP_TYPE_ANY)
                W = img1.GetWidth()
                H = img1.GetHeight()
                img1 = img1.Scale(int(W * self.resize_factor), int(H * self.resize_factor))
                img1_bm = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img1))
                path2 = image_path + list_of_pieces[2][i] + image_format
                img2 = wx.Image(path2, wx.BITMAP_TYPE_ANY)
                W = img2.GetWidth()
                H = img2.GetHeight()
                img2 = img2.Scale(int(W * self.resize_factor), int(H * self.resize_factor))
                img2_bm = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img2))

                vsizer.Add(img1_bm, 1, wx.ALL, 5)
                vsizer.Add(img2_bm, 1, wx.ALL, 5)

                self.hsizer_tech_tracks.Add(vsizer, 1, wx.EXPAND | wx.ALL)

                #panel.SetSizer(vsizer)
                #self.hsizer_tech_tracks.Add(panel, 1, wx.EXPAND | wx.ALL)





        vsizer_output.Add(self.hsizer_tech_tracks, 1, wx.EXPAND | wx.ALL, 5)
        vsizer_output.Add(self.hsizer_extra_tech, 1, wx.EXPAND | wx.ALL, 5)
        vsizer_output.Add(self.hsizer_round_score, 1, wx.EXPAND | wx.ALL, 5)
        vsizer_output.Add(self.hsizer_boosters, 1, wx.EXPAND | wx.ALL, 5)

        self.hsizer_output.Add(vsizer_output, 1, wx.EXPAND | wx.ALL, 5)
        self.vsizer_overall.Add(self.hsizer_output, 0, wx.EXPAND)

        self.SetSizer(self.vsizer_overall)


    def on_randomize(self, event):
        overall_vsizer = wx.BoxSizer(wx.VERTICAL)

        for i in range(len(list_of_pieces)):
            random.shuffle(list_of_pieces[i])

        for i in range(6):
            if i == 0: # Brown
                hsizer = wx.BoxSizer(wx.HORIZONTAL)
                brown_vsizer1 = wx.BoxSizer(wx.VERTICAL)
                brown_vsizer2 = wx.BoxSizer(wx.VERTICAL)

                path = image_path + list_of_pieces[0][0] + image_format
                brown_fed = wx.Image(path, wx.BITMAP_TYPE_ANY)
                brown_fed_image = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(brown_fed))
                brown_vsizer1.Add(brown_fed_image, 0, wx.ALL, 5)

                path1 = image_path + list_of_pieces[1][i] + image_format
                img1 = wx.Image(path1, wx.BITMAP_TYPE_ANY)
                img1_bm = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img1))
                path2 = image_path + list_of_pieces[2][i] + image_format
                img2 = wx.Image(path2, wx.BITMAP_TYPE_ANY)
                img2_bm = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img2))

                brown_vsizer2.Add(img1_bm, 0, wx.ALL, 5)
                brown_vsizer2.Add(img2_bm, 0, wx.ALL, 5)

                hsizer.Add(brown_vsizer1, 1, wx.ALL, 5)
                hsizer.Add(brown_vsizer2, 1, wx.ALL, 5)
                self.hsizer_tech_tracks.Add(hsizer, 1, wx.EXPAND | wx.ALL, 20)
            else:
                vsizer = wx.BoxSizer(wx.VERTICAL)

                path1 = image_path + list_of_pieces[1][i] + image_format
                img1 = wx.Image(path1, wx.BITMAP_TYPE_ANY)
                img1_bm = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img1))
                path2 = image_path + list_of_pieces[2][i] + image_format
                img2 = wx.Image(path2, wx.BITMAP_TYPE_ANY)
                img2_bm = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img2))

                vsizer.Add(img1_bm, 0, wx.ALL, 5)
                vsizer.Add(img2_bm, 0, wx.ALL, 5)
                self.hsizer_tech_tracks.Add(vsizer, 1, wx.EXPAND | wx.ALL, 20)

        n_players = int(self.players_number.GetValue())
        num_boosters = n_players + 3

        # Tech tile distribution
        row_1 = list_of_pieces[2][0:6]
        row_2 = list_of_pieces[2][6:9]

        list_of_pieces[2] = row_1
        list_of_pieces[3] = row_2

if __name__ == "__main__":
    app = wx.App()
    MainFrame()
    app.MainLoop()
