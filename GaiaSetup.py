import wx
import wx.grid
import random
from Gaia import Map

demo_map_path = "images/MapDemo.png"
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


class MainFrame(wx.Frame):
    def __init__(self, parent=None):
        super(MainFrame, self).__init__(parent, title="Gaia Setup", size=(1200, 850))
        self.default_font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.make_menu()
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.SetFont(self.default_font)

        self.default_num_players = 2
        self.SetBackgroundColour(wx.WHITE)

        #icon

        vsizer = wx.BoxSizer(wx.VERTICAL)

        hsizer_main = wx.BoxSizer(wx.HORIZONTAL)
        vsizer_player_info = wx.BoxSizer(wx.VERTICAL)

        players_info_text = wx.StaticText(self, -1, "Number of players")
        self.players_number = wx.TextCtrl(self, value=str(self.default_num_players))
        btn_make_map = wx.Button(self, wx.ID_ADD, label="Generate map", size=(120, 40))
        self.Bind(wx.EVT_BUTTON, self.on_make_map, btn_make_map)
        btn_randomize = wx.Button(self, wx.ID_PAGE_SETUP, label="Randomize setup", size=(140, 40))
        self.Bind(wx.EVT_BUTTON, self.on_randomize, btn_randomize)

        vsizer_player_info.Add(players_info_text, 1)
        vsizer_player_info.Add(self.players_number, 1)

        hsizer_main.Add(vsizer_player_info, 1, wx.EXPAND | wx.ALL, 20)
        hsizer_main.Add(btn_make_map, 1, wx.EXPAND | wx.ALL, 20)
        hsizer_main.Add(btn_randomize, 1, wx.EXPAND | wx.ALL, 20)

        vsizer.Add(hsizer_main, 0, wx.EXPAND)

        self.SetSizer(vsizer)
        self.Centre()
        self.Show()

    def on_randomize(self, event):
        n_players = int(self.players_number.GetValue())
        random_setup = RandomSetup(self, n_players)
        random_setup.Show(True)

    def on_make_map(self, event):
        n_players = int(self.players_number.GetValue())

        map = MapGenerator(self, n_players)
        map.Show(True)

    def make_menu(self):
        pass

    def on_close(self, event):
        self.Destroy()

    def get_default_num_players(self):
        return self.default_num_players

class MapGenerator(wx.Frame):
    def __init__(self, parent, num_players, image_path=default_map_path):
        super(MapGenerator, self).__init__(parent, title="Map Generator", size=(1050, 850))
        num_players = num_players

        PhotoMaxHeight = 800
        self.SetBackgroundColour(wx.WHITE)

        map = Map(num_players)
        map.save_image_map()

        img = wx.Image(image_path, wx.BITMAP_TYPE_ANY)
        W = img.GetWidth()
        H = img.GetHeight()
        NewH = PhotoMaxHeight
        NewW = PhotoMaxHeight * W / H

        img = img.Scale(NewW, NewH)
        imageMap = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img))

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(imageMap, 0, wx.ALL, 5)

        self.SetSizer(hsizer)

        self.Centre()
        self.Show()


class RandomSetup(wx.Frame):
    def __init__(self, parent, num_players):
        super(RandomSetup, self).__init__(parent, title="Random setup", size=(1200, 950))
        resize_factor = 0.8

        hsizer_output = wx.BoxSizer(wx.HORIZONTAL)
        vsizer_overall = wx.BoxSizer(wx.VERTICAL)

        vsizer_output = wx.BoxSizer(wx.VERTICAL)

        hsizer_tech_tracks = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_extra_tech = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_boosters = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_round_score = wx.BoxSizer(wx.HORIZONTAL)
        vsizer_end_score = wx.BoxSizer(wx.VERTICAL)

        htracks = [hsizer_tech_tracks, hsizer_extra_tech, hsizer_round_score, hsizer_boosters]

        background = wx.Image(background_path, wx.BITMAP_TYPE_ANY)
        background_img = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(background))

        for i, list in enumerate(list_of_pieces):
            random.shuffle(list)

        for i in range(6):
            if i == 0:  # Brown
                hsizer = wx.BoxSizer(wx.HORIZONTAL)
                brown_vsizer1 = wx.BoxSizer(wx.VERTICAL)
                brown_vsizer2 = wx.BoxSizer(wx.VERTICAL)

                path = image_path + list_of_pieces[0][0] + image_format
                brown_fed = wx.Image(path, wx.BITMAP_TYPE_ANY)
                W = brown_fed.GetWidth()
                H = brown_fed.GetHeight()
                local_factor = 0.8
                brown_fed = brown_fed.Scale(int(W * resize_factor * local_factor),
                                            int(H * resize_factor * local_factor))
                brown_fed_image = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(brown_fed))
                brown_vsizer1.Add(brown_fed_image, 1, wx.ALL)

                path1 = image_path + list_of_pieces[1][i] + image_format
                img1 = wx.Image(path1, wx.BITMAP_TYPE_ANY)
                W = img1.GetWidth()
                H = img1.GetHeight()
                img1 = img1.Scale(int(W * resize_factor), int(H * resize_factor))
                img1_bm = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img1))
                path2 = image_path + list_of_pieces[2][i] + image_format
                img2 = wx.Image(path2, wx.BITMAP_TYPE_ANY)
                W = img2.GetWidth()
                H = img2.GetHeight()
                img2 = img2.Scale(int(W * resize_factor), int(H * resize_factor))
                img2_bm = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img2))

                brown_vsizer2.Add(img1_bm, 1, wx.ALL, 5)
                brown_vsizer2.Add(img2_bm, 1, wx.ALL, 5)

                hsizer.Add(brown_vsizer1, 1, wx.ALL)
                hsizer.Add(brown_vsizer2, 1, wx.ALL)

                hsizer_tech_tracks.Add(hsizer, 1, wx.EXPAND | wx.ALL)

            else: # all other tracks
                vsizer = wx.BoxSizer(wx.VERTICAL)

                path1 = image_path + list_of_pieces[1][i] + image_format
                img1 = wx.Image(path1, wx.BITMAP_TYPE_ANY)
                W = img1.GetWidth()
                H = img1.GetHeight()
                img1 = img1.Scale(int(W * resize_factor), int(H * resize_factor))
                img1_bm = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img1))
                path2 = image_path + list_of_pieces[2][i] + image_format
                img2 = wx.Image(path2, wx.BITMAP_TYPE_ANY)
                W = img2.GetWidth()
                H = img2.GetHeight()
                img2 = img2.Scale(int(W * resize_factor), int(H * resize_factor))
                img2_bm = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img2))

                vsizer.Add(img1_bm, 1, wx.ALL, 5)
                vsizer.Add(img2_bm, 1, wx.ALL, 5)

                hsizer_tech_tracks.Add(vsizer, 1, wx.EXPAND | wx.ALL)

        vsizer_output.Add(hsizer_tech_tracks, 1, wx.EXPAND | wx.ALL, 5)

        # Extra tech tiles
        extra_tech = list_of_pieces[2][6:9]

        for i in range(len(extra_tech)):
            path = image_path + extra_tech[i] + image_format
            img = wx.Image(path, wx.BITMAP_TYPE_ANY)
            W = img.GetWidth()
            H = img.GetHeight()
            img = img.Scale(int(W * resize_factor), int(H * resize_factor))
            img_bm = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img))

            hsizer_extra_tech.Add(img_bm, 1, wx.ALL, 5)

        vsizer_output.Add(hsizer_extra_tech, 1, wx.EXPAND | wx.ALL, 5)

        # Boosters
        num_boosters = num_players + 3

        for i in range(num_boosters):
            path = image_path + list_of_pieces[4][i] + image_format
            img = wx.Image(path, wx.BITMAP_TYPE_ANY)
            W = img.GetWidth()
            H = img.GetHeight()
            img = img.Scale(int(W * resize_factor), int(H * resize_factor))
            img_bm = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img))

            hsizer_boosters.Add(img_bm, 1, wx.ALL, 5)

        vsizer_output.Add(hsizer_boosters, 1, wx.EXPAND | wx.ALL, 5)

        # Round score
        for i in range(6):
            path = image_path + list_of_pieces[5][i] + image_format
            img = wx.Image(path, wx.BITMAP_TYPE_ANY)
            W = img.GetWidth()
            H = img.GetHeight()
            img = img.Scale(int(W * resize_factor), int(H * resize_factor))
            img_bm = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img))

            hsizer_round_score.Add(img_bm, 1, wx.ALL, 5)

        # End game score
        for i in range(2):
            path = image_path + list_of_pieces[6][i] + image_format
            img = wx.Image(path, wx.BITMAP_TYPE_ANY)
            W = img.GetWidth()
            H = img.GetHeight()
            img = img.Scale(int(W * resize_factor), int(H * resize_factor))
            img_bm = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img))

            vsizer_end_score.Add(img_bm, 1, wx.ALL, 5)

        hsizer_round_score.Add(vsizer_end_score, 1, wx.ALL, 5)
        vsizer_output.Add(hsizer_round_score, 1, wx.EXPAND | wx.ALL, 5)

        hsizer_output.Add(vsizer_output, 1, wx.EXPAND | wx.ALL, 5)
        vsizer_overall.Add(hsizer_output, 0, wx.EXPAND)

        self.SetSizer(vsizer_overall)

        self.Centre()
        self.Show()

if __name__ == "__main__":
    app = wx.App()
    MainFrame()
    app.MainLoop()
