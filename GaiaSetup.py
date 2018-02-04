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

terra_param = [1.0, 1.0, 0.1, 0.8]
gaia_param = 1.0
trans_param = 0.5
range_factor = [1.0, 1.0, 0.6, 0.05]

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

        hsizer_main.Add(vsizer_player_info, 1, wx.EXPAND | wx.ALL, 10)
        hsizer_main.Add(btn_make_map, 1, wx.EXPAND | wx.ALL, 10)
        hsizer_main.Add(btn_randomize, 1, wx.EXPAND | wx.ALL, 10)

        vsizer.Add(hsizer_main, 0, wx.EXPAND)

        # Setup
        hsizer_setup = wx.BoxSizer(wx.HORIZONTAL)
        vsizer_setup = wx.BoxSizer(wx.VERTICAL)
        vsizer_setup_2 = wx.BoxSizer(wx.VERTICAL)
        vsizer_info = wx.BoxSizer(wx.VERTICAL)

        methods = ["Neighbors", "Distribution", "Big clusters"]
        method_box = wx.RadioBox(self, label="Optimization method", choices=methods)
        vsizer_setup.Add(method_box, -1, wx.EXPAND | wx.ALL, 10)

        hsizer_iterations = wx.BoxSizer(wx.HORIZONTAL)
        num_iterations_txt = wx.StaticText(self, 0, "Number of iterations")
        num_iterations = wx.TextCtrl(self, value=str(10)) # TODO: set default

        hsizer_iterations.Add(num_iterations_txt, 3, wx.EXPAND | wx.ALL, 5)
        hsizer_iterations.Add(num_iterations, 1)
        vsizer_setup_2.Add(hsizer_iterations, 1, wx.EXPAND | wx.ALL)

        hsizer_cluster = wx.BoxSizer(wx.HORIZONTAL)
        cluster_txt = wx.StaticText(self, 0, "Max cluster size")
        cluster_size = wx.TextCtrl(self, value=str(4))  # TODO: set default

        hsizer_cluster.Add(cluster_txt, 3, wx.EXPAND | wx.ALL, 5)
        hsizer_cluster.Add(cluster_size, 1)
        vsizer_setup_2.Add(hsizer_cluster, 1, wx.EXPAND | wx.ALL)

        hsizer_neighbor = wx.BoxSizer(wx.HORIZONTAL)
        neighbor_txt = wx.StaticText(self, 0, "Minimum distance between equal planets")
        min_neighbor_distance = wx.TextCtrl(self, value=str(2))  # TODO: set default

        hsizer_neighbor.Add(neighbor_txt, 3, wx.EXPAND | wx.ALL, 5)
        hsizer_neighbor.Add(min_neighbor_distance, 1)
        vsizer_setup_2.Add(hsizer_neighbor, 1, wx.EXPAND | wx.ALL)

        vsizer_setup.Add(vsizer_setup_2, 1, wx.EXPAND | wx.ALL, 10)

        hsizer_core = wx.BoxSizer(wx.HORIZONTAL)
        core_txt = wx.StaticText(self, 0, "Keep core sectors")
        rb_core_yes = wx.RadioButton(self, label="Yes", style=wx.RB_GROUP)
        rb_core_no = wx.RadioButton(self, label="No")
        rb_core_no.SetValue(True)

        hsizer_core.Add(core_txt, 6)
        hsizer_core.Add(rb_core_yes, 1)
        hsizer_core.Add(rb_core_no, 1)
        vsizer_setup.Add(hsizer_core, -1, wx.EXPAND | wx.ALL, 10)

        hsizer_center = wx.BoxSizer(wx.HORIZONTAL)
        center_txt = wx.StaticText(self, 0, "2-player: Do not allow hex 6 in centre")
        rb_center_yes = wx.RadioButton(self, label="Yes", style=wx.RB_GROUP)
        rb_center_no = wx.RadioButton(self, label="No")
        rb_center_no.SetValue(True)

        hsizer_center.Add(center_txt, 6)
        hsizer_center.Add(rb_center_yes, 1)
        hsizer_center.Add(rb_center_no, 1)
        vsizer_setup.Add(hsizer_center, -1, wx.EXPAND | wx.ALL, 10)

        hsizer_small = wx.BoxSizer(wx.HORIZONTAL)
        small_txt = wx.StaticText(self, 0, "3-player: Smaller map")
        rb_small_yes = wx.RadioButton(self, label="Yes", style=wx.RB_GROUP)
        rb_small_no = wx.RadioButton(self, label="No")
        rb_small_no.SetValue(True)

        hsizer_small.Add(small_txt, 6)
        hsizer_small.Add(rb_small_yes, 1)
        hsizer_small.Add(rb_small_no, 1)
        vsizer_setup.Add(hsizer_small, -1, wx.EXPAND | wx.ALL, 10)

        # Neighbors method
        vsizer_neighbors = wx.BoxSizer(wx.VERTICAL)
        method_neighbor_txt = wx.StaticText(self, 0, "Neighbors method")
        vsizer_neighbors.Add(method_neighbor_txt, 1, wx.EXPAND | wx.ALL, 5)

        hsizer_terra = wx.BoxSizer(wx.HORIZONTAL)
        terra_txt = wx.StaticText(self, 0, "Terra parameters [home, 1, 2, 3]:")
        terra_home = wx.TextCtrl(self, value=str(1.0), size=(50, -1))  # TODO: set default
        terra_1 = wx.TextCtrl(self, value=str(1.0), size=(50, -1))  # TODO: set default
        terra_2 = wx.TextCtrl(self, value=str(0.1), size=(50, -1))  # TODO: set default
        terra_3 = wx.TextCtrl(self, value=str(0.8), size=(50, -1))  # TODO: set default

        hsizer_terra.Add(terra_txt, 1, wx.EXPAND | wx.ALL, 5)
        hsizer_terra.Add(terra_home, -1)
        hsizer_terra.Add(terra_1, -1)
        hsizer_terra.Add(terra_2, -1)
        hsizer_terra.Add(terra_3, -1)
        vsizer_neighbors.Add(hsizer_terra, 1, wx.EXPAND | wx.ALL, 5)

        hsizer_gaia = wx.BoxSizer(wx.HORIZONTAL)
        gaia_txt = wx.StaticText(self, 0, "Gaia parameter:")
        gaia_param = wx.TextCtrl(self, value=str(1.0))  # TODO: set default

        hsizer_gaia.Add(gaia_txt, 3, wx.EXPAND | wx.ALL, 5)
        hsizer_gaia.Add(gaia_param, 1)
        vsizer_neighbors.Add(hsizer_gaia, 1, wx.EXPAND | wx.ALL, 5)

        hsizer_trans = wx.BoxSizer(wx.HORIZONTAL)
        trans_txt = wx.StaticText(self, 0, "Trans dimentional parameter:")
        trans_param = wx.TextCtrl(self, value=str(0.5))  # TODO: set default

        hsizer_trans.Add(trans_txt, 3, wx.EXPAND | wx.ALL, 5)
        hsizer_trans.Add(trans_param, 1)
        vsizer_neighbors.Add(hsizer_trans, 1, wx.EXPAND | wx.ALL, 5)

        hsizer_range = wx.BoxSizer(wx.HORIZONTAL)
        range_txt = wx.StaticText(self, 0, "Range parameters [1, 2, 3]:")
        range_1 = wx.TextCtrl(self, value=str(1.0), size=(50, -1))  # TODO: set default
        range_2 = wx.TextCtrl(self, value=str(0.6), size=(50, -1))  # TODO: set default
        range_3 = wx.TextCtrl(self, value=str(0.005), size=(50, -1))  # TODO: set default

        hsizer_range.Add(range_txt, 1, wx.EXPAND | wx.ALL, 5)
        hsizer_range.Add(range_1, -1)
        hsizer_range.Add(range_2, -1)
        hsizer_range.Add(range_3, -1)
        vsizer_neighbors.Add(hsizer_range, 1, wx.EXPAND | wx.ALL, 5)

        vsizer_setup.Add(vsizer_neighbors, 1, wx.EXPAND | wx.ALL, 5)

        # Distribution method
        vsizer_distribution = wx.BoxSizer(wx.VERTICAL)
        method_distribution_txt = wx.StaticText(self, 0, "Distribution method")
        vsizer_distribution.Add(method_distribution_txt, 1, wx.EXPAND | wx.ALL, 5)

        hsizer_nearness = wx.BoxSizer(wx.HORIZONTAL)
        nearness_txt = wx.StaticText(self, 0, "Nearness weight:")
        nearness_param = wx.TextCtrl(self, value=str(0.5))  # TODO: set default

        hsizer_nearness.Add(nearness_txt, 3, wx.EXPAND | wx.ALL, 5)
        hsizer_nearness.Add(nearness_param, 1)
        vsizer_distribution.Add(hsizer_nearness, 1, wx.EXPAND | wx.ALL, 5)

        hsizer_density = wx.BoxSizer(wx.HORIZONTAL)
        density_txt = wx.StaticText(self, 0, "Planet Density Dropoff Scale:")
        density_param = wx.TextCtrl(self, value=str(0.5))  # TODO: set default

        hsizer_density.Add(density_txt, 3, wx.EXPAND | wx.ALL, 5)
        hsizer_density.Add(density_param, 1)
        vsizer_distribution.Add(hsizer_density, 1, wx.EXPAND | wx.ALL, 5)

        hsizer_ratio = wx.BoxSizer(wx.HORIZONTAL)
        ratio_txt = wx.StaticText(self, 0, "Type Ratio Dropoff Scale:")
        ratio_param = wx.TextCtrl(self, value=str(0.5))  # TODO: set default

        hsizer_ratio.Add(ratio_txt, 3, wx.EXPAND | wx.ALL, 5)
        hsizer_ratio.Add(ratio_param, 1)
        vsizer_distribution.Add(hsizer_ratio, 1, wx.EXPAND | wx.ALL, 5)

        vsizer_setup.Add(vsizer_distribution, 1, wx.EXPAND | wx.ALL, 5)

        info = """
        Methods:
        - Neighbors: Optimize for planet neighbors based on priority factors
        - Distribution: Even distribution of planets based on prioritized parameters
        - Big clusters: Optimize for large average cluster sizes
        
        Number of iterations:
            - how many legal maps to evaluate
            
        Relevant neighbor radius:
            - 0 is planets own location
            
        Max cluster size:
            - min value of 3 (recommended 4 or greater)
            
        Minimum distance between equal planets:
            - not included gaia (default: min 2) and transdim planets
            
        Keep core sectors
            - Sectors 1, 2, 3 and 4 in kept in the centre ()
            
        2-player: Do not allow hex 6 in centre
            - Few planets in this sector
            
        3-player: Smaller map
            - Use only two hexes in row 2
            
        Parameters - Neighbors method:
            - terra_param: preference of neighbors based on terraforming distance
            - gaia_param: preference of gaia planet nearby
            - trans_param: preference of trans dimentional planet nearby
            - range_factor: value of planet based on distance (radius)
        
        Parameters - Distribution method:
            - Nearness weight (0-1): planet density vs planet type TODO: what is 1.0
            - Planet Density Dropoff Scale (0-inf): Ideal density priority
            - Type Ratio Dropoff Scale (0-inf): Ideal planet distribution priority        
        
        """

        info_text = wx.StaticText(self, 1, info)
        vsizer_info.Add(info_text, 1, wx.EXPAND | wx.ALL, 20)

        hsizer_setup.Add(vsizer_setup, 1, wx.EXPAND)
        hsizer_setup.Add(vsizer_info, 1, wx.EXPAND)

        vsizer.Add(hsizer_setup, 0, wx.EXPAND)
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
        # optimize
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
