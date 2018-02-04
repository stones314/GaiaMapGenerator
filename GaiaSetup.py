import wx
import wx.grid
import random
from Gaia import Map
import copy

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

default_num_players = 2
default_num_iterations = 1000
default_radius = 2
default_cluster_size = 4
default_min_neighbor_distance = 2

default_terra_param = [1.0, 1.0, 0.1, 0.8]
default_gaia_param = 1.0
default_trans_param = 0.5
default_range_factor = [1.0, 1.0, 0.6, 0.05]

default_nearness_param = 0.5
default_density_param = 40
default_ratio_param = 7


class MainFrame(wx.Frame):
    def __init__(self, parent=None):
        super(MainFrame, self).__init__(parent, title="Gaia Setup", size=(1200, 850))
        self.default_font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.bold_font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.make_menu()
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.SetFont(self.default_font)

        self.abort = False
        self.SetBackgroundColour(wx.WHITE)
        self.quality_description = ""

        ico = wx.Icon('images/gaia_icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)

        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer_main = wx.BoxSizer(wx.HORIZONTAL)
        vsizer_player_info = wx.BoxSizer(wx.VERTICAL)

        players_info_text = wx.StaticText(self, -1, "Number of players")
        self.num_players = wx.TextCtrl(self, value=str(default_num_players))
        btn_make_map = wx.Button(self, wx.ID_ADD, label="Generate map", size=(120, 40))
        self.Bind(wx.EVT_BUTTON, self.on_make_map, btn_make_map)
        btn_randomize = wx.Button(self, wx.ID_PAGE_SETUP, label="Randomize setup", size=(140, 40))
        self.Bind(wx.EVT_BUTTON, self.on_randomize, btn_randomize)
        self.progress = wx.StaticText(self, 0, str("Map progress: 0%"))
        self.balance = wx.StaticText(self, 0, str(""))
        self.btn_abort = wx.Button(self, wx.ID_ABORT, label="Stop", size=(80, 40))
        self.Bind(wx.EVT_BUTTON, self.on_abort, self.btn_abort)

        self.enable_abort_btn(False)

        vsizer_player_info.Add(players_info_text, 1)
        vsizer_player_info.Add(self.num_players, 1)

        vsizer_progress = wx.BoxSizer(wx.VERTICAL)
        vsizer_progress.Add(self.progress, 1, wx.EXPAND | wx.ALL)
        vsizer_progress.Add(self.balance, 1, wx.EXPAND | wx.ALL)

        hsizer_main.Add(vsizer_player_info, 1, wx.EXPAND | wx.ALL, 10)
        hsizer_main.Add(btn_make_map, 2, wx.EXPAND | wx.ALL, 10)
        hsizer_main.Add(btn_randomize, 2, wx.EXPAND | wx.ALL, 10)
        hsizer_main.Add(vsizer_progress, 1, wx.EXPAND | wx.ALL, 20)
        hsizer_main.Add(self.btn_abort, 1, wx.EXPAND | wx.ALL, 10)


        vsizer.Add(hsizer_main, 0, wx.EXPAND)

        # Setup
        hsizer_setup = wx.BoxSizer(wx.HORIZONTAL)
        vsizer_setup = wx.BoxSizer(wx.VERTICAL)
        vsizer_setup_2 = wx.BoxSizer(wx.VERTICAL)
        vsizer_info = wx.BoxSizer(wx.VERTICAL)

        methods = ["Neighbors", "Distribution", "Big clusters"]
        self.method_box = wx.RadioBox(self, label="Optimization method", choices=methods)
        vsizer_setup.Add(self.method_box, -1, wx.EXPAND | wx.ALL, 10)

        hsizer_iterations = wx.BoxSizer(wx.HORIZONTAL)
        num_iterations_txt = wx.StaticText(self, 0, "Number of iterations")
        self.num_iterations = wx.TextCtrl(self, value=str(default_num_iterations))

        hsizer_iterations.Add(num_iterations_txt, 3, wx.EXPAND | wx.ALL, 5)
        hsizer_iterations.Add(self.num_iterations, 1)
        vsizer_setup_2.Add(hsizer_iterations, 1, wx.EXPAND | wx.ALL)

        hsizer_radius = wx.BoxSizer(wx.HORIZONTAL)
        radius_txt = wx.StaticText(self, 0, "Relevant neighbor radius")
        self.radius = wx.TextCtrl(self, value=str(default_radius))

        hsizer_radius.Add(radius_txt, 3, wx.EXPAND | wx.ALL, 5)
        hsizer_radius.Add(self.radius, 1)
        vsizer_setup_2.Add(hsizer_radius, 1, wx.EXPAND | wx.ALL)

        hsizer_cluster = wx.BoxSizer(wx.HORIZONTAL)
        cluster_txt = wx.StaticText(self, 0, "Max cluster size")
        self.cluster_size = wx.TextCtrl(self, value=str(default_cluster_size))

        hsizer_cluster.Add(cluster_txt, 3, wx.EXPAND | wx.ALL, 5)
        hsizer_cluster.Add(self.cluster_size, 1)
        vsizer_setup_2.Add(hsizer_cluster, 1, wx.EXPAND | wx.ALL)

        hsizer_neighbor = wx.BoxSizer(wx.HORIZONTAL)
        neighbor_txt = wx.StaticText(self, 0, "Minimum distance between equal planets")
        self.min_neighbor_distance = wx.TextCtrl(self, value=str(default_min_neighbor_distance))

        hsizer_neighbor.Add(neighbor_txt, 3, wx.EXPAND | wx.ALL, 5)
        hsizer_neighbor.Add(self.min_neighbor_distance, 1)
        vsizer_setup_2.Add(hsizer_neighbor, 1, wx.EXPAND | wx.ALL)

        vsizer_setup.Add(vsizer_setup_2, 1, wx.EXPAND | wx.ALL, 10)

        hsizer_core = wx.BoxSizer(wx.HORIZONTAL)
        core_txt = wx.StaticText(self, 0, "Keep core sectors")
        self.rb_core_yes = wx.RadioButton(self, label="Yes", style=wx.RB_GROUP)
        rb_core_no = wx.RadioButton(self, label="No")
        rb_core_no.SetValue(True)

        hsizer_core.Add(core_txt, 6)
        hsizer_core.Add(self.rb_core_yes, 1)
        hsizer_core.Add(rb_core_no, 1)
        vsizer_setup.Add(hsizer_core, -1, wx.EXPAND | wx.ALL, 10)

        hsizer_center = wx.BoxSizer(wx.HORIZONTAL)
        center_txt = wx.StaticText(self, 0, "2-player: Disable hex 6 in centre")
        self.rb_center_yes = wx.RadioButton(self, label="Yes", style=wx.RB_GROUP)
        rb_center_no = wx.RadioButton(self, label="No")
        rb_center_no.SetValue(True)

        hsizer_center.Add(center_txt, 6)
        hsizer_center.Add(self.rb_center_yes, 1)
        hsizer_center.Add(rb_center_no, 1)
        vsizer_setup.Add(hsizer_center, -1, wx.EXPAND | wx.ALL, 10)

        hsizer_small = wx.BoxSizer(wx.HORIZONTAL)
        small_txt = wx.StaticText(self, 0, "3-player: Smaller map")
        self.rb_small_yes = wx.RadioButton(self, label="Yes", style=wx.RB_GROUP)
        rb_small_no = wx.RadioButton(self, label="No")
        rb_small_no.SetValue(True)

        hsizer_small.Add(small_txt, 6)
        hsizer_small.Add(self.rb_small_yes, 1)
        hsizer_small.Add(rb_small_no, 1)
        vsizer_setup.Add(hsizer_small, -1, wx.EXPAND | wx.ALL, 10)

        # Neighbors method
        vsizer_neighbors = wx.BoxSizer(wx.VERTICAL)
        method_neighbor_txt = wx.StaticText(self, 0, "Neighbors method")
        method_neighbor_txt.SetFont(self.bold_font)
        vsizer_neighbors.Add(method_neighbor_txt, 1, wx.EXPAND | wx.ALL, 5)

        hsizer_terra = wx.BoxSizer(wx.HORIZONTAL)
        terra_txt = wx.StaticText(self, 0, "Terra parameters [home, 1, 2, 3]:")
        self.terra_home = wx.TextCtrl(self, value=str(default_terra_param[0]), size=(50, -1))
        self.terra_1 = wx.TextCtrl(self, value=str(default_terra_param[1]), size=(50, -1))
        self.terra_2 = wx.TextCtrl(self, value=str(default_terra_param[2]), size=(50, -1))
        self.terra_3 = wx.TextCtrl(self, value=str(default_terra_param[3]), size=(50, -1))

        hsizer_terra.Add(terra_txt, 1, wx.EXPAND | wx.ALL, 5)
        hsizer_terra.Add(self.terra_home, -1)
        hsizer_terra.Add(self.terra_1, -1)
        hsizer_terra.Add(self.terra_2, -1)
        hsizer_terra.Add(self.terra_3, -1)
        vsizer_neighbors.Add(hsizer_terra, 1, wx.EXPAND | wx.ALL, 5)

        hsizer_gaia = wx.BoxSizer(wx.HORIZONTAL)
        gaia_txt = wx.StaticText(self, 0, "Gaia parameter:")
        self.gaia_param = wx.TextCtrl(self, value=str(default_gaia_param))

        hsizer_gaia.Add(gaia_txt, 3, wx.EXPAND | wx.ALL, 5)
        hsizer_gaia.Add(self.gaia_param, 1)
        vsizer_neighbors.Add(hsizer_gaia, 1, wx.EXPAND | wx.ALL, 5)

        hsizer_trans = wx.BoxSizer(wx.HORIZONTAL)
        trans_txt = wx.StaticText(self, 0, "Trans dimentional parameter:")
        self.trans_param = wx.TextCtrl(self, value=str(default_trans_param))

        hsizer_trans.Add(trans_txt, 3, wx.EXPAND | wx.ALL, 5)
        hsizer_trans.Add(self.trans_param, 1)
        vsizer_neighbors.Add(hsizer_trans, 1, wx.EXPAND | wx.ALL, 5)

        hsizer_range = wx.BoxSizer(wx.HORIZONTAL)
        range_txt = wx.StaticText(self, 0, "Range parameters [1, 2, 3]:")
        self.range_1 = wx.TextCtrl(self, value=str(default_range_factor[1]), size=(50, -1))
        self.range_2 = wx.TextCtrl(self, value=str(default_range_factor[2]), size=(50, -1))
        self.range_3 = wx.TextCtrl(self, value=str(default_range_factor[3]), size=(50, -1))

        hsizer_range.Add(range_txt, 1, wx.EXPAND | wx.ALL, 5)
        hsizer_range.Add(self.range_1, -1)
        hsizer_range.Add(self.range_2, -1)
        hsizer_range.Add(self.range_3, -1)
        vsizer_neighbors.Add(hsizer_range, 1, wx.EXPAND | wx.ALL, 5)

        vsizer_setup.Add(vsizer_neighbors, 1, wx.EXPAND | wx.ALL, 5)

        # Distribution method
        vsizer_distribution = wx.BoxSizer(wx.VERTICAL)
        method_distribution_txt = wx.StaticText(self, 0, "Distribution method")
        method_distribution_txt.SetFont(self.bold_font)
        vsizer_distribution.Add(method_distribution_txt, 1, wx.EXPAND | wx.ALL, 5)

        hsizer_nearness = wx.BoxSizer(wx.HORIZONTAL)
        nearness_txt = wx.StaticText(self, 0, "Nearness weight:")
        self.nearness_param = wx.TextCtrl(self, value=str(default_nearness_param))

        hsizer_nearness.Add(nearness_txt, 3, wx.EXPAND | wx.ALL, 5)
        hsizer_nearness.Add(self.nearness_param, 1)
        vsizer_distribution.Add(hsizer_nearness, 1, wx.EXPAND | wx.ALL, 5)

        hsizer_density = wx.BoxSizer(wx.HORIZONTAL)
        density_txt = wx.StaticText(self, 0, "Planet Density Dropoff Scale:")
        self.density_param = wx.TextCtrl(self, value=str(default_density_param))

        hsizer_density.Add(density_txt, 3, wx.EXPAND | wx.ALL, 5)
        hsizer_density.Add(self.density_param, 1)
        vsizer_distribution.Add(hsizer_density, 1, wx.EXPAND | wx.ALL, 5)

        hsizer_ratio = wx.BoxSizer(wx.HORIZONTAL)
        ratio_txt = wx.StaticText(self, 0, "Type Ratio Dropoff Scale:")
        self.ratio_param = wx.TextCtrl(self, value=str(default_ratio_param))

        hsizer_ratio.Add(ratio_txt, 3, wx.EXPAND | wx.ALL, 5)
        hsizer_ratio.Add(self.ratio_param, 1)
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
            - not included gaia (using 2 as minimum) and transdim planets
            
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
            - Nearness weight (0-1): planet density (1.0) vs planet type (0.0)
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
        n_players = int(self.num_players.GetValue())
        random_setup = RandomSetup(self, n_players)
        random_setup.Show(True)

    def on_make_map(self, event):
        n_players = int(self.num_players.GetValue())
        if n_players < 2 or n_players > 4:
            self.num_players.SetValue(str(default_num_players))
            self.on_error("Number of players must be 2, 3 or 4")
            return

        keep_core = (True if self.rb_core_yes.GetValue() else False)
        disable_six_in_centre = (True if self.rb_center_yes.GetValue() else False)
        smaller_map = (True if self.rb_small_yes.GetValue() else False)

        if disable_six_in_centre:
            if n_players == 2:
                disable_six_in_centre = True
            else:
                disable_six_in_centre = False

        if smaller_map:
            if n_players == 3:
                smaller_map = True
            else:
                smaller_map = False

        map = Map(n_players, True, keep_core, disable_six_in_centre, smaller_map)

        method = self.method_box.GetSelection()
        num_iteration = int(self.num_iterations.GetValue())
        if num_iteration < 100:
            self.num_iterations.SetValue(str(default_num_iterations))
            self.on_error("Number of iterations has to be more than 100.")
            return

        radius = int(self.radius.GetValue())
        if radius < 1 or radius > 3:
            self.radius.SetValue(str(default_radius))
            self.on_error("Radius must be between 1 and 3")
            return

        cluster_size = int(self.cluster_size.GetValue())
        if cluster_size < 3:
            self.cluster_size.SetValue(str(default_cluster_size))
            self.on_error("Maximum cluster size must be greater than 2")
            return

        min_neighbor_distance = int(self.min_neighbor_distance.GetValue())
        if min_neighbor_distance > 4:
            self.min_neighbor_distance.SetValue(default_min_neighbor_distance)
            self.on_error("Minimum distance between planets of equal color can not be greater than 4")
            return

        terra_param = [float(self.terra_home.GetValue()), float(self.terra_1.GetValue()),
                       float(self.terra_2.GetValue()), float(self.terra_3.GetValue())]
        gaia_param = float(self.gaia_param.GetValue())
        trans_param = float(self.trans_param.GetValue())
        range_factor = [1.0, float(self.range_1.GetValue()),
                        float(self.range_2.GetValue()), float(self.range_3.GetValue())]

        neighbor_params = copy.deepcopy(terra_param)
        neighbor_params.append(gaia_param)
        neighbor_params.append(trans_param)
        neighbor_params.extend(range_factor)

        for param in neighbor_params:
            if param > 1 or param < 0:
                self.on_error("All parameters within the Neighbor Method must be between 0 and 1")
                return

        nearness_param = float(self.nearness_param.GetValue())

        if nearness_param < 0 or nearness_param > 1:
            self.on_error("Nearness weight must be between 0 and 1")
            return

        density_param = float(self.density_param.GetValue())

        if density_param < 0:
            self.on_error("Planet Density Dropoff Scale must be greater than 0")
            return

        ratio_param = float(self.ratio_param.GetValue())

        if ratio_param < 0:
            self.on_error("Type Ratio Dropoff Scale must be greater than 0")
            return

        map.set_method(method)
        map.set_try_count(num_iteration)
        map.set_search_radius(radius)
        map.set_max_cluster_size(cluster_size)
        map.set_minimum_equal_range(min_neighbor_distance)

        if method == 0: #
            map.set_method_0_params(terra_param, gaia_param, trans_param, range_factor)
            self.quality_description = "Variance"
        elif method == 1:
            map.set_method_1_params(nearness_param, density_param, ratio_param)
            self.quality_description = "Quality"
        elif method == 2:
            self.quality_description = "Av. size"

        self.enable_abort_btn(True)
        map.balance_map(self.set_progress, self.should_abort)
        map.set_to_balanced_map()

        map_setup = MapSetup(self, map)
        map_setup.Show(True)

        self.set_progress(0, 0)
        self.abort = False

    def make_menu(self):
        pass

    def on_close(self, event):
        self.Destroy()

    def get_default_num_players(self):
        return self.default_num_players

    def set_progress(self, progress, balance):
        wx.Yield()
        self.quality_description
        if progress == 0:
            self.progress.SetLabel("Map progress: 0%")
            self.balance.SetLabel(self.quality_description + ": NA")
        elif progress < 100:
            self.progress.SetLabel("Map progress: " + str(progress) + "%")
            self.balance.SetLabel(self.quality_description  + ": {:06.4f}".format(balance))
        else:
            self.enable_abort_btn(False)
            self.progress.SetLabel("Creating image...")
            self.balance.SetLabel(self.quality_description  + ": {:06.4f}".format(balance))

    def enable_abort_btn(self, boolean):
        if boolean:
            self.btn_abort.SetBackgroundColour(wx.RED)
            self.btn_abort.Enable()
        else:
            self.btn_abort.SetBackgroundColour(None)
            self.btn_abort.Disable()

    def should_abort(self):
        return self.abort

    def on_abort(self, event=None):
        self.abort = True

    def on_error(self, error_message):
        PopupWindow(self, error_message, "WARNING", (300, 200))

class MapSetup(wx.Frame):
    def __init__(self, parent, map, image_path=default_map_path):
        super(MapSetup, self).__init__(parent, title="Map Generator", size=(1050, 850))

        ico = wx.Icon('images/hexagon_icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)

        PhotoMaxHeight = 800
        self.SetBackgroundColour(wx.WHITE)

        map.save_image_map()
        # TODO: add save function to popup window with map

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

        ico = wx.Icon('images/tech_icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
        self.SetBackgroundColour("#FFFFFF")

        hsizer_output = wx.BoxSizer(wx.HORIZONTAL)
        vsizer_overall = wx.BoxSizer(wx.VERTICAL)

        vsizer_output = wx.BoxSizer(wx.VERTICAL)

        hsizer_tech_tracks = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_extra_tech = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_boosters = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_round_score = wx.BoxSizer(wx.HORIZONTAL)
        vsizer_end_score = wx.BoxSizer(wx.VERTICAL)
        hsizer_round_and_end_score = wx.BoxSizer(wx.HORIZONTAL)

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

                hsizer_tech_tracks.Add(hsizer, 1, wx.EXPAND | wx.ALL, 0)
                hsizer_tech_tracks.AddSpacer(20)

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

        hsizer_round_and_end_score.Add(hsizer_round_score, 1, wx.ALL, 30)
        hsizer_round_and_end_score.Add(vsizer_end_score, 1, wx.ALL, 5)
        vsizer_output.Add(hsizer_round_and_end_score, 1, wx.EXPAND | wx.ALL, 5)

        hsizer_output.Add(vsizer_output, 1, wx.EXPAND | wx.ALL, 5)
        vsizer_overall.Add(hsizer_output, 0, wx.EXPAND)

        self.SetSizer(vsizer_overall)

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

        self.Centre()
        self.Show()

    def OnEraseBackground(self, event):
        dc = event.GetDC()

        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)

        dc.Clear()
        bmp = wx.Bitmap(background_path)
        dc.DrawBitmap(bmp, 0, 0)


class PopupWindow(wx.PopupWindow):
    def __init__(self, parent, message, header_txt = None, size=(500, 300)):
        wx.PopupWindow.__init__(self, parent, wx.SIMPLE_BORDER)

        default_font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.SetFont(default_font)

        self.SetSize(size)
        width = size[0]
        height = size[1]

        if header_txt:
            header_font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
            header = wx.TextCtrl(self, -1, header_txt, pos=(20, 20), style=wx.TE_READONLY | wx.BORDER_NONE)
            header.SetFont(header_font)

            text = wx.TextCtrl(self, -1, message, size=(width - 40, height - 110), pos=(20, 50),
                               style=wx.TE_READONLY | wx.TE_MULTILINE | wx.BORDER_NONE)
        else:
            text = wx.TextCtrl(self, -1, message, size=(width - 40, height - 80), pos=(20, 20),
                               style=wx.TE_READONLY | wx.TE_MULTILINE | wx.BORDER_NONE)

        text.SetBackgroundColour("#f0f0f0")

        close_btn = wx.Button(self, wx.ID_CLOSE, label="Close", pos=(width - 120, height - 60), size=(100, 40))
        self.Bind(wx.EVT_BUTTON, self.on_close, close_btn)

        self.CenterOnParent(dir=wx.BOTH)
        self.Show()

    def on_close(self, event):
        self.Destroy()


if __name__ == "__main__":
    app = wx.App()
    MainFrame()
    app.MainLoop()
