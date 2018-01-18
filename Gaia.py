from PIL import Image
import random
import copy
import os

"""
Planets = {"Em" : Empty(), "Ga" : Gaia(), "Tr" : Transdim(),
           "Br" : Brown(), "Bl" : Blue(), "Bk" : Black(),
           "Ye" : Yellow(), "Or" : Orange(), "Re" : Red(), "Wh" : White()}
"""

Sector_data = {
    "1": [["Em"],
          ["Em", "Bl", "Em", "Em", "Em", "Br"],
          ["Em", "Em", "Em", "Tr", "Em", "Or", "Re", "Em", "Em", "Ye", "Em", "Em"]],
    "2": [["Em"],
          ["Em", "Wh", "Em", "Em", "Br", "Em"],
          ["Bk", "Em", "Em", "Ye", "Em", "Tr", "Em", "Re", "Em", "Em", "Em", "Or"]],
    "3": [["Em"],
          ["Em", "Em", "Wh", "Em", "Em", "Ga"],
          ["Tr", "Em", "Em", "Bk", "Em", "Em", "Ye", "Bl", "Em", "Em", "Em", "Em"]],
    "4": [["Em"],
          ["Re", "Em", "Br", "Em", "Or", "Em"],
          ["Bk", "Em", "Em", "Em", "Bl", "Em", "Em", "Em", "Em", "Wh", "Em", "Em"]],
    "5": [["Em"],
          ["Em", "Em", "Em", "Em", "Em", "Ga"],
          ["Wh", "Em", "Tr", "Re", "Em", "Em", "Ye", "Or", "Em", "Em", "Em", "Em"]],
    "6": [["Em"],
          ["Em", "Bl", "Em", "Ga", "Em", "Br"],
          ["Em", "Tr", "Em", "Em", "Ye", "Tr", "Em", "Em", "Em", "Em", "Em", "Em"]],
    "7": [["Em"],
          ["Re", "Em", "Ga", "Em", "Ga", "Em"],
          ["Em", "Br", "Em", "Em", "Em", "Em", "Bk", "Em", "Em", "Em", "Tr", "Em"]],
    "8": [["Em"],
          ["Wh", "Em", "Bk", "Em", "Or", "Em"],
          ["Bl", "Em", "Tr", "Em", "Em", "Em", "Em", "Tr", "Em", "Em", "Em", "Em"]],
    "9": [["Em"],
          ["Em", "Em", "Ga", "Em", "Bk", "Em"],
          ["Em", "Tr", "Wh", "Em", "Em", "Em", "Em", "Em", "Br", "Em", "Em", "Or"]],
    "10": [["Em"],
           ["Em", "Em", "Ga", "Em", "Em", "Ye"],
           ["Em", "Tr", "Tr", "Em", "Em", "Em", "Em", "Re", "Bl", "Em", "Em", "Em"]],
    "5_": [["Em"],
           ["Em", "Em", "Em", "Em", "Em", "Ga"],
           ["Wh", "Em", "Tr", "Re", "Em", "Em", "Em", "Or", "Em", "Em", "Em", "Em"]],
    "6_": [["Em"],
           ["Em", "Bl", "Em", "Ga", "Em", "Em"],
           ["Em", "Tr", "Em", "Em", "Ye", "Tr", "Em", "Em", "Em", "Em", "Em", "Em"]],
    "7_": [["Em"],
           ["Ga", "Em", "Br", "Em", "Ga", "Em"],
           ["Em", "Em", "Em", "Em", "Em", "Em", "Bk", "Em", "Em", "Em", "Tr", "Em"]]
}

color_wheel = ["Bk", "Br", "Ye", "Or", "Re", "Bl", "Wh"]


def get_dist(hex_a_coord, hex_b_coord):
    """
  Function that get the distance between two hexes
  """
    dist = 0
    col = hex_a_coord[0]
    row = hex_a_coord[1]
    while row - hex_b_coord[1] != 0 or col - hex_b_coord[0] != 0:
        if col - hex_b_coord[0] == 0:
            if row - hex_b_coord[1] < 0:
                row = row + 2
            else:
                row = row - 2
        else:
            if col - hex_b_coord[0] < 0:
                col = col + 1
            else:
                col = col - 1
            if row - hex_b_coord[1] < 0:
                row = row + 1
            else:
                row = row - 1
        dist = dist + 1
    return dist


def get_hexes_at_radius(centre_col, centre_row, radius):
    """
  Function that get a list of all hexes at a certain radius from
  a centre hex
  """
    if radius == 0:
        hex_list = [[centre_col, centre_row]]
        return hex_list
    if radius == 1:
        hex_list = [[centre_col, centre_row - 2],
                    [centre_col + 1, centre_row - 1],
                    [centre_col + 1, centre_row + 1],
                    [centre_col, centre_row + 2],
                    [centre_col - 1, centre_row + 1],
                    [centre_col - 1, centre_row - 1]]
        return hex_list
    if radius == 2:
        hex_list = [[centre_col, centre_row - 4],
                    [centre_col + 1, centre_row - 3],
                    [centre_col + 2, centre_row - 2],
                    [centre_col + 2, centre_row],
                    [centre_col + 2, centre_row + 2],
                    [centre_col + 1, centre_row + 3],
                    [centre_col, centre_row + 4],
                    [centre_col - 1, centre_row + 3],
                    [centre_col - 2, centre_row + 2],
                    [centre_col - 2, centre_row],
                    [centre_col - 2, centre_row - 2],
                    [centre_col - 1, centre_row - 3]]
        return hex_list
    if radius == 3:
        hex_list = [[centre_col, centre_row - 6],
                    [centre_col + 1, centre_row - 5],
                    [centre_col + 2, centre_row - 4],
                    [centre_col + 3, centre_row - 3],
                    [centre_col + 3, centre_row - 1],
                    [centre_col + 3, centre_row + 1],
                    [centre_col + 3, centre_row + 3],
                    [centre_col + 2, centre_row + 4],
                    [centre_col + 1, centre_row + 5],
                    [centre_col, centre_row + 6],
                    [centre_col - 1, centre_row + 5],
                    [centre_col - 2, centre_row + 4],
                    [centre_col - 3, centre_row + 3],
                    [centre_col - 3, centre_row + 1],
                    [centre_col - 3, centre_row - 1],
                    [centre_col - 3, centre_row - 3],
                    [centre_col - 2, centre_row - 4],
                    [centre_col - 1, centre_row - 5]]
        return hex_list
    return []


def get_planet_coords(planet_type, hex_map):
    """
  Function that loops through map and finds plantes of the same type
  Returns a list of the positions of these planets
  -planet_type is the planet type string (e.g "Bk")
  -hex_map is the map of the galaxy represented as a list of cols
  """
    coords = []
    n_cols = len(hex_map)
    if n_cols < 1:
        return coords
    n_rows = len(hex_map[0])
    if n_rows < 1:
        return coords
    for col in range(n_cols):
        for row in range(n_rows):  # looping through the map
            if hex_map[col][row] == planet_type:  # looking for planets of the right types
                coords.append([col, row])
    return coords


def get_hex_distances(hex_coords):
    """
  Function that finds distances between coords
  Given a list of coords it returns a list of all the distances between these coords
  A list with N coords will lead to a list of (N-1) + (N - 2) + ... + 1 = N*(N-1)/2 distances
  """
    n = len(hex_coords)
    if n < 2:
        return []
    distances = [0] * (n * (n - 1) / 2)
    i = 0
    for c1 in range(n - 1):
        for c2 in range(c1 + 1, n):
            distances[i] = get_dist(hex_coords[c1], hex_coords[c2])
            i += 1
    return distances


def get_stats(values):
    """
  Function to calculate statistics from a list of values
  Returns a list of results as follows:
  0 - average
  1 - variance
  2 - min value
  3 - max value
  """
    values.sort()
    avg = 0.0
    var = 0.0
    minv = 0
    maxv = 0
    n = len(values)
    if n < 1:
        return [avg, var, minv, maxv]
    if n < 2:
        return [values[0], var, values[0], values[0]]
    for val in values:
        avg = avg + val
    avg = avg / n
    for val in values:
        diff = val - avg
        var = var + diff * diff
    var = var / n
    return [avg, var, values[0], values[n - 1]]


def has_equal_neigbours(hex_map):
    """
  Function that loops through hex map and checks if there are
  any equal planet types next to each other (ignoring Transdimentional planets and voids)
  returns 0 if no eaqual neighbours exist
          1 if any equal neighbours exists
"""
    n_cols = len(hex_map)
    if n_cols < 1:
        return 0
    n_rows = len(hex_map[0])
    if n_rows < 1:
        return 0
    for col in range(n_cols):
        for row in range(n_rows):  # looping through the map
            if hex_map[col][row] == "Tr" or hex_map[col][row] is None or hex_map[col][row] == "Em":
                continue
            neighbours = get_hexes_at_radius(col, row, 1)
            for i in range(2,
                           4):  # only look at neighbours "in front of" the planet, or we would check some stuff more than once
                if neighbours[i][0] >= n_cols or neighbours[i][1] >= n_rows:
                    continue  # in case we are at the end of a col/row
                if hex_map[col][row] == hex_map[neighbours[i][0]][neighbours[i][1]]:
                    return 1
    return 0


def get_color_dist(planet1, planet2):
    """
  Function that finds the distance between two planets on the color wheel
  """
    if planet1 == planet2:
        return 0
    if planet1 == "Ga" or planet2 == "Ga":
        return 1
    if planet1 == "Tr" or planet2 == "Tr":
        return 3
    first = -1
    second = -1
    for i in range(7):
        if color_wheel[i] == planet1 or color_wheel[i] == planet2:
            if first == -1:
                first = i
            else:
                second = i
                break
    dist = second - first
    if dist > 3:
        dist = 7 - dist
    return dist


def calc_happiness(planet_type, hex_map, GP, TP, HP, max_range, RF):
    """
  Function that calculates happiness for a planet type
  It loops through the map and sums the happiness of each
  planet of that type
  Happiness is determined as follows:
   - Gaia planet at range R adds happiness GP/R
   - Transdim planet at range R adds happiness TP/R
   - Other planet at range R adds happiness CP[CD]/R,
     where CD is the color distance to that planet.
     Hence CP is a list with 4 elements [cp0,cp1,cp2,cp3],
     giving the happiness for planets at color distance 0-3
   - Only planets within max_range is included
  """
    happiness = 0.0
    n_cols = len(hex_map)
    if n_cols < 1:
        return happiness
    n_rows = len(hex_map[0])
    if n_rows < 1:
        return happiness
    n_data = 0
    for col in range(n_cols):
        for row in range(n_rows):
            if hex_map[col][row] == planet_type:
                for R in range(1, max_range+1):
                    coords = get_hexes_at_radius(col, row, R)
                    for coord in coords:
                        if coord[0] < 0 or coord[0] >= n_cols:
                            continue
                        if coord[1] < 0 or coord[1] >= n_rows:
                            continue
                        if hex_map[coord[0]][coord[1]] is None or hex_map[coord[0]][coord[1]] == "Em":
                            continue
                        if hex_map[coord[0]][coord[1]] == "Ga":
                            happiness += GP * RF[R]
                        elif hex_map[coord[0]][coord[1]] == "Tr":
                            happiness += TP * RF[R]
                        else:
                            color_dist = get_color_dist(hex_map[col][row], hex_map[coord[0]][coord[1]])
                            happiness += HP[color_dist] * RF[R]
                        n_data += 1
    return happiness #/ n_data #not sure if we shoul "normalize" value or not... (if it makes sense)


def get_cluster_size_list(hex_map, ignored_types=[None, "Em"]):
    '''
  Method that iterates over the map and finds clusters of planets
  It returns a list containing the size of each cluster
  The length of that list is then the number of clusters
  A single planet with no neighbours is a cluster of size 1
  ignored_types is a list of hex content types that should not be part of a cluster,
  defaults to [None,"Em"]
  '''
    n_cols = len(hex_map)
    n_rows = len(hex_map[0])
    cluster_sizes = []
    n_clusters = 0
    visited = [[0 for i in range(n_rows)] for j in range(n_cols)]
    for col in range(n_cols):
        for row in range(n_rows):
            if hex_map[col][row] in ignored_types:
                visited[col][row] = 1
                continue
            if visited[col][row] == 1:
                continue

            # at this point we are at a planet in a hex that has not already been visited
            # it is the start of a new cluster
            n_clusters += 1
            cluster_sizes.append(0)
            cluster_planets = [[col, row]]
            i = 0
            while i < len(cluster_planets):
                planet_col = cluster_planets[i][0]
                planet_row = cluster_planets[i][1]
                i += 1
                if visited[planet_col][planet_row] == 1:
                    # need to check this here since it might have been visited after it was added to cluster_planets
                    continue

                # at a new planet, cluster grows:
                cluster_sizes[n_clusters - 1] += 1
                visited[planet_col][planet_row] = 1

                # check outwards for neighbour planets:
                neighbour_hexes = get_hexes_at_radius(planet_col, planet_row, 1)
                for j in range(6):
                    neighbour_col = neighbour_hexes[j][0]
                    neighbour_row = neighbour_hexes[j][1]
                    if (visited[neighbour_col][neighbour_row] == 1) or (
                            hex_map[neighbour_col][neighbour_row] in ignored_types):
                        # ignore neighbour hex if it has been visited already or if it has an ignorable type of content
                        continue
                    cluster_planets.append(neighbour_hexes[j])

    return cluster_sizes


class Map(object):
    def __init__(self, players, random="Yes"):
        """
        2-player: 2-3-2, hex 1, 2, 3, 4, 5_,6_,7_ (6_ not in centre)
        3- and 4-player: 3-4-3, hex 1, 2, 3, 4, 5, 6, 7, 8, 9, 10

        centre (x, y) - (hor, ver)

        self.map: Sector objects
        self.map_data: Tupple with sector number and rotation
        """

        self.players = players
        self.random = random
        self.map = None
        self.width = 23
        self.height = 30


        self.convert = {"Em": Empty, "Tr": Fancy_planet, "Ga": Fancy_planet,
                        "Br": Planet, "Bl": Planet, "Bk": Planet,
                        "Ye": Planet, "Or": Planet, "Re": Planet, "Wh": Planet}

        self.set_map()
        self.generate_full_map()

        #parameter used in optimization
        self.try_count = 100
        self.best_balance = 100000.0
        self.best_map_data = self.get_printable_map_data()

        # parameters used in the happiness calculation:
        self.max_range = 3
        self.range_factor = [1.0, 1.0, 0.8, 0.4]
        self.terraform_param = [3.0, 2.0, 1.0, 1.0]
        self.gaia_param = 2.0
        self.trans_param = 1.0

    def set_map(self):
        Small = ["1", "5_", "2", "3", "6_", "4", "7_"]
        Large = ["10", "1", "5", "9", "2", "3", "6", "8", "4", "7"]
        index = 0
        default_sector_rotation = 0

        if self.players == 2:
            self.map = [["A", "B"], ["C", "D", "E"], ["F", "G"]]
            self.centre = [[(6, 6), (11, 7)], [(3, 13), (8, 14), (13, 15)], [(5, 21), (10, 22)]]
            if self.random == "Yes":
                random.shuffle(Small)
                #Commented out: in person we dont want hex 6 to be centre tile. For now we will let it be possible
                #for the map gen. TODO: maybe make it an input parameter?
                #if Small[3] == "6_":
                #    centre = Small[0]
                #    Small[0] = Small[3]
                #    Small[3] = centre
            self.content = Small
        else:
            self.map = [["A", "B", "C"], ["D", "E", "F", "G"], ["H", "I", "J"]]
            self.centre = [[(6, 6), (11, 7), (16, 8)], [(3, 13), (8, 14), (13, 15), (18, 16)],
                           [(5, 21), (10, 22), (15, 23)]]
            if self.random == "Yes":
                random.shuffle(Large)
            self.content = Large

        for j, row in enumerate(self.map):
            for i, item in enumerate(row):
                sector_number = self.content[index]
                sector_content = Sector_data[sector_number]
                self.map[j][i] = Sector(sector_content, sector_number)
                index += 1

    def generate_full_map(self):
        self.full_map = [[None for i in range(self.height)] for j in range(self.width)]
        for j, row in enumerate(self.map):
            for i, sector in enumerate(row):
                content = sector.get_content()
                position = self.centre[j][i]
                rel_coor = sector.get_relative_coord()

                for radii, planet_list in enumerate(content):
                    planet_coord_list = get_hexes_at_radius(position[0], position[1], radii)
                    for number, hexagon in enumerate(planet_list):
                        self.full_map[planet_coord_list[number][0]][planet_coord_list[number][1]] = hexagon

    def print_map(self):
        print "---------------------"
        n_col = len(self.full_map)
        n_row = len(self.full_map[0])
        for row in range(n_row):
            cont = []
            for col in range(n_col):
                cont.append(self.full_map[col][row])
            print cont
        print "---------------------"

    def make_image_map(self, clockwise=True):
        """
        sector list = [(sector, rotation)]
        """
        sector_list = self.get_printable_map_data()
        image_location = "images/"
        image_format = ".png"

        image_width = 1884
        image_height = 2042

        map_width = int(image_width * len(sector_list[1]) * 0.96)
        map_height = int(image_height * 2.8)

        map_picture = Image.new("RGB", (map_width, map_height), (255, 255, 255))

        height_adjustment = int(image_height * 0.1)
        vscale = 0.71
        hscale = 0.945

        sector_start_horizontal = int(image_width * 0.56)
        sector_start_vertical = 0

        v_offsets = [0, 0, int(image_height * 0.1)]
        h_offsets = [sector_start_horizontal, 0, sector_start_horizontal - int(image_width * 0.18)]

        for j, row in enumerate(sector_list):
            for i, (sector_number, sector_rotation) in enumerate(row):
                filename = image_location + sector_number + image_format
                hor = h_offsets[j] + int(image_width * hscale * i)
                ver = v_offsets[j] + (int(image_height * vscale * j)) + sector_start_vertical + height_adjustment * i
                image = Image.open(filename)
                image = image.rotate(-sector_rotation)
                map_picture.paste(image, (hor, ver), image)

        map_picture.show()

    def rotate_map_randomly(self):
        for row in self.map:
            for sector in row:
                n_rot = random.randint(0, 5)
                sector.rotate_sector(n_rot)
        self.generate_full_map()
        if has_equal_neigbours(self.full_map) == 1:
            self.rotate_map_randomly()

    def get_printable_map_data(self):
        """
        returns map data that is easy for image creation
        """
        map_data = copy.deepcopy(self.map)
        for j, row in enumerate(self.map):
            for i, sector in enumerate(row):
                sector_rotation = sector.get_rotation_deg()
                sector_number = sector.get_id()
                map_data[j][i] = [sector_number, sector_rotation]
        return map_data

    def get_full_map(self):
        return self.full_map

    def set_try_count(self, try_count):
        self.try_count = try_count

    def set_max_range(self, max_range):
        self.max_range = max_range

    def set_range_factor(self, range_factor):
        self.range_factor = range_factor

    def set_terraform_param(self, terraform_param):
        self.terraform_param = terraform_param

    def set_gaia_param(self, gaia_param):
        self.gaia_param = gaia_param

    def set_trans_param(self, trans_param):
        self.trans_param = trans_param

    def calculate_balance(self, print_happiness=0):
        planet_happiness = [0.0] * 7
        for i in range(7):
            planet_happiness[i] = calc_happiness(color_wheel[i],
                                                 self.full_map,
                                                 self.gaia_param,
                                                 self.trans_param,
                                                 self.terraform_param,
                                                 self.max_range,
                                                 self.range_factor)
        stats = get_stats(planet_happiness)

        if print_happiness != 0:
            print color_wheel
            print planet_happiness
            print stats
        return stats[1]

    def balance_map(self):
        self.best_balance = self.calculate_balance()
        self.best_map_data = self.get_printable_map_data()
        progress = 0
        for i in range(self.try_count):
            #if self.try_count%(self.try_count/10) == 0:
            #    print "progress = " + str(progress)
            #    progress += 10
            self.rotate_map_randomly()
            balance = self.calculate_balance()
            if balance < self.best_balance:
                self.best_balance = balance
                self.best_map_data = self.get_printable_map_data()


    def get_best_map_data(self):
        return self.best_map_data

    def set_map_by_map_data(self, map_data):
        for j, row in enumerate(self.map):
            for i, sector in enumerate(row):
                sector_rotation = map_data[j][i][1]
                while sector.get_rotation_deg() != sector_rotation:
                    sector.rotate_sector_once()
        self.generate_full_map()

    def set_to_balanced_map(self):
        self.set_map_by_map_data(self.best_map_data)


class Sector(object):
    def __init__(self, content, ID):
        """
            2.11    2.12    2.01
        2.10    1.6     1.1     2.02
    2.09    1.5     0.0     1.2     2.03
        2.08    1.4     1.3     2.04
            2.07    2.06    2.05

        content =  [[0.0],
                    [1.1, 1.2, 1.3, 1.4, 1.5, 1.6],
                    [2.01, 2.02, 2.03, 2.04, 2.05, 2.06, 2.07, 2.08, 2.09, 2.10, 2.11, 2.12]]
        
        """

        self.content = content
        self.rotation = 0
        self.ID = ID

        self.relative_coordinates = [[(0, 0)],
                                     [(0, +2), (+1, -1), (+1, +1), (+0, -2), (-1, +1), (-1, -1)],
                                     [(-0, -4), (+1, -3), (+2, -2), (+2, -0), (+2, +2), (+1, +3), (0, +4), (-1, +3),
                                      (-2, +2), (-2, 0), (-2, -2), (-1, -3)]]

    def rotate_sector(self, num_rotations):
        for i in range(num_rotations):
            self.rotate_sector_once()

    def rotate_sector_once(self):
        original_sector = copy.deepcopy(self.content)
        for j, row in enumerate(self.content):
            if j == 0:
                pass
            else:
                for i, item in enumerate(row):
                    self.content[j][(i + j) % (6 * j)] = original_sector[j][i]
        self.rotation += 1
        if self.rotation == 6:
            self.rotation = 0

    def get_content(self):
        return self.content

    def get_relative_coord(self):
        return self.relative_coordinates

    def get_rotation_deg(self):
        return self.rotation * 60

    def get_id(self):
        return self.ID


class Hexagon(object):
    def __init__(self, planet_type=None, sector_number=None, coordinate=None):
        if planet_type == None:
            self.type = "Em"
        else:
            self.type = planet_type

        self.sector_number = sector_number
        self.coordinate = coordinate

    def type(self):
        return self.type


class Empty(Hexagon):
    def __init__(self, planet_type=None, sector_number=None, coordinate=None):
        pass


class Fancy_planet(Hexagon):
    def __init__(self, planet_type=None, sector_number=None, coordinate=None):
        pass


class Planet(Hexagon):
    def __init__(self, planet_type, sector_number, coordinate):
        self.type = planet_type
        first = {"Ga": 0, "Tr": 0, "Br": 0, "Bl": 0, "Bk": 0, "Ye": 0, "Or": 0, "Re": 0, "Wh": 0}
        second = {"Ga": 0, "Tr": 0, "Br": 0, "Bl": 0, "Bk": 0, "Ye": 0, "Or": 0, "Re": 0, "Wh": 0}
        third = {"Ga": 0, "Tr": 0, "Br": 0, "Bl": 0, "Bk": 0, "Ye": 0, "Or": 0, "Re": 0, "Wh": 0}

    def evaluate(colour):
        """
        first - planet one step away
        second - planet two steps away
        third - planet three steps away

        input: colour to evaluate
        output: score for that colour
        """
        first = {"Ga": 0, "Tr": 0, "Br": 0, "Bl": 0, "Bk": 0, "Ye": 0, "Or": 0, "Re": 0, "Wh": 0}
        second = {"Ga": 0, "Tr": 0, "Br": 0, "Bl": 0, "Bk": 0, "Ye": 0, "Or": 0, "Re": 0, "Wh": 0}
        third = {"Ga": 0, "Tr": 0, "Br": 0, "Bl": 0, "Bk": 0, "Ye": 0, "Or": 0, "Re": 0, "Wh": 0}

        score = 0

        return score



if __name__ == "__main__":
    test_map = Map(4, "No")
    test_map.set_try_count(100)

    test_map.balance_map()
    test_map.set_to_balanced_map()
    test_map.calculate_balance(1)
    test_map.make_image_map(test_map.get_best_map_data())
    hex_map = test_map.get_full_map()

    '''
    for i in range(7):
        planet_coords = get_planet_coords(color_wheel[i], hex_map)
        distances = get_hex_distances(planet_coords)
        stats = get_stats(distances)
        print "Stats for " + color_wheel[i] + ":"
        print " - Number of planets:    " + str(len(planet_coords))
        print " - Average dist between: " + str(stats[0])
        print " - Variance in dist:     " + str(stats[1])
        print " - Minimum distance:     " + str(stats[2])
        print " - Maximum distance:     " + str(stats[3])
    '''
    clusters = get_cluster_size_list(hex_map)
    clusters.sort()
    print clusters

