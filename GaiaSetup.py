import wx
import wx.grid
from Gaia import Map

demo_map_path = "images/MapDemo.png"
standard_map_path = "images/StandardMap.png"
default_map_path = "images/MapDemo.png"

class MainFrame(wx.Frame):
    def __init__(self, parent=None):
        super(MainFrame, self).__init__(parent, title="Gaia Setup", size=(850, 850))
        self.default_font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.make_menu()
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.SetFont(self.default_font)

        #icon

        self.panel = wx.Panel(self)
        self.notebook = NotebookStructure(self, self.panel)
        self.map_tab = self.notebook.get_map_tab()

        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(self.notebook, 1, wx.ALL | wx.EXPAND, 5)
        self.panel.SetSizer(vsizer)
        self.Centre()
        self.Show()

    def make_menu(self):
        pass

    def on_close(self, event):
        self.Destroy()

class NotebookStructure(wx.Notebook):
    def __init__(self, parent, panel):
        wx.Notebook.__init__(self, panel, id=wx.ID_ANY, style=wx.BK_DEFAULT)
        self.parent = parent
        self.map_tab = MapTab(self)

        self.AddPage(self.map_tab, "Map")

    def get_map_tab(self):
        return self.map_tab

class MapTab(wx.Panel):
    def __init__(self, parent):
        super(MapTab, self).__init__(parent=parent, id=wx.ID_ANY)
        self.parent = parent
        self.png = None
        self.default_num_players = 4
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
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img))

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
        self.hsizer2.Add(self.imageCtrl, 0, wx.ALL, 5)
        self.vsizer2.Add(self.hsizer, 0)    # setup
        self.vsizer2.Add(self.hsizer2, 0, wx.EXPAND)

        self.SetSizer(self.vsizer2)

    def on_make_map(self, event):
        n_players = self.players_number.GetValue()
        self.map = Map(n_players)
        self.map.make_image_map(self.map.map_data)

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
        self.imageCtrl.SetBitmap(wx.Bitmap(img))

if __name__ == "__main__":
    app = wx.App()
    MainFrame()
    app.MainLoop()
