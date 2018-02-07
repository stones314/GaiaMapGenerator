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
    avg = 0.0
    var = 0.0
    minv = 100000.0
    maxv = -100000.0
    n = len(values)
    if n < 1:
        return [avg, var, minv, maxv]
    if n < 2:
        return [values[0], var, values[0], values[0]]
    for val in values:
        avg = avg + val
        if val < minv:
            minv = val
        if val > maxv:
            maxv = val
    avg = avg / n
    for val in values:
        diff = val - avg
        var = var + diff * diff
    var = var / n
    return [avg, var, minv, maxv]


def has_equal_neigbours(hex_map, radius=2):
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
            for R in range(1, radius+1):
                if R > 1 and hex_map[col][row] == "Ga":
                    break
                neighbours = get_hexes_at_radius(col, row, R)
                for coords in neighbours:
                    if coords[0] < 0 or coords[1] < 0:
                        continue # in case we are outside the map
                    if coords[0] >= n_cols or coords[1] >= n_rows:
                        continue  # in case we are at the end of a col/row
                    if hex_map[col][row] == hex_map[coords[0]][coords[1]]:
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
    """
    Method that iterates over the map and finds clusters of planets
    It returns a list containing the size of each cluster
    The length of that list is then the number of clusters
    A single planet with no neighbours is a cluster of size 1
    ignored_types is a list of hex content types that should not be part of a cluster,
    defaults to [None,"Em"]
    """
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


def number_factor(PD, SC=30.0, OD=0.32153):
    """
    PD - Planet density
    OD - Optimal density
    SC - a number used to scale how bad it is to differ from the
         optimal density. Lower number means less bad
    Returns a number between 0.0 and 1.0 indicating how good the
    density of planets is compared to the optimal density
    """
    diff_from_opt = OD - PD
    exponent = -SC * diff_from_opt * diff_from_opt
    return pow(2.718281828, exponent)


def type_factor(NT, NP, SC=30.0):
    """
    NT - Number of planet types in area
    NP - Number of planets in area
    SC - a number used to scale how bad it is to differ from the
         optimal number of planet types. Lower number means less bad
    Returns a number between 0.0 and 1.0 indicating how good the ratio
    of different planet types is compared to the optimal ratio
    The optimal is to have as many different planet types as possible
    """
    max_types = 9.0
    if NP < max_types:
        max_types = NP
    ratio = 0.0
    if max_types > 0.0:
        ratio = NT / max_types
    diff_from_opt = 1.0 - ratio
    exponent = -SC * diff_from_opt * diff_from_opt
    return pow(2.718281828, exponent)


def hex_happiness(col, row, hex_map, NW=0.5, PD_SC=30.0, TR_SC=30.0, radius=3):
    """
    col - column of centre hex
    row - row of centre hex
    hex_map - the map..
    NW - how much weight should be placed on planet density vs planet type
    PD_SC - Planet Density Dropoff Scale. Higher number means that happiness drops
         off faster as the planet density moves away from the ideal density
    TR_SC - Type Ratio Dropoff Scale. Higher number means that the happiness drops
         off faster as the ratio of different planet types moves away from maximum
         ratio = (number of different planet types)/(number of different planet types possible)
    radius - radius used for each hex when calculatin hex happiness

    Optimal density of planets is about 1/3 in the full map
    as there are 61 planets divided on 190 hexes (0.321053)
    This means that inside a sector of range R there should be about
     2 planets when  R = 1 ( 7 total hexes, density = 0.285714)
     6 planets when  R = 2 (19 total hexes, density = 0.315789)
     12 planets when R = 3 (37 total hexes, density = 0.324324)
    We want a nice distribution of planet types through the space,
    so that for any sector with R = 3 we want as many planet types
    as possible to exist inside that sector.
    Given these factors we define hex happiness as follows:
     H = NW*number_factor(PD) + (1-NW)*type_factor(NT,NP)
    where
     NP - number of planets inside max_range
     PD - planet density in area = NP/(number of hexes in area)
     NT - number of unique planet types inside range 3
     NW - how much weight should be placed on number of planets
          vs nymber of types. NW must be a number between 0.0 and 1.0
     number_factor() is a formula that returns a maximum value of 1.0
          for the optimal number of planets, and smaller values for
          number of planets further away from the optimum
     type_factor() is a  formula that returns a maximum value of 1.0
          for the optimal number of planet types, and smaller values for
          number of planet types further away from the optimum
    The resulting value should be a number between 0.0 and 1.0
    """
    planet_types = ["Bl", "Br", "Ye", "Or", "Re", "Bl", "Wh", "Ga", "Tr"]
    n_planet_types = len(planet_types)
    exists_in_range = [0.0 for i in range(n_planet_types)]
    NH = 0.0
    n_cols = len(hex_map)
    n_rows = len(hex_map[0])
    for R in range(radius + 1):
        coords = get_hexes_at_radius(col, row, R)
        for coord in coords:
            if coord[0] < 0 or coord[0] >= n_cols:
                continue
            if coord[1] < 0 or coord[1] >= n_rows:
                continue
            PT = hex_map[coord[0]][coord[1]]
            if PT is not None:
                NH += 1.0
                for i in range(n_planet_types):
                    if planet_types[i] == PT:
                        exists_in_range[i] += 1.0
                        break
    NP = 0.0
    NT = 0.0
    for i in range(n_planet_types):
        if exists_in_range[i] > 0:
            NT += 1.0
            NP += exists_in_range[i]
    PD = NP / NH

    return NW * number_factor(PD, PD_SC) + (1.0 - NW) * type_factor(NT, NP, TR_SC)


def calc_map_happiness(hex_map, NW=0.5, PD_SC=30.0, TR_SC=5.0, radius=3):
    """
    hex_map - the map used in the calculation
    PD_SC - Planet Density Dropoff Scale. Higher number means that happiness drops
         off faster as the planet density moves away from the ideal density
    TR_SC - Type Ratio Dropoff Scale. Higher number means that the happiness drops
         off faster as the ratio of different planet types moves away from maximum
         ratio = (number of different planet types)/(number of different planet types possible)
    radius - radius used for each hex when calculatin hex happiness

    Iterates over the hex_map and calculates total happiness (sum of happiness for each hex)
    Returns a vector with the following data
     0 - happiness percentage
     1 - total happiness
     3 - number of hexes calculated for (changes depending on map size)
    """
    total_happiness = 0.0
    n_hexes = 0.0
    n_cols = len(hex_map)
    n_rows = len(hex_map[0])
    for col in range(n_cols):
        for row in range(n_rows):
            if hex_map[col][row] is None:
                continue
            total_happiness += hex_happiness(col, row, hex_map, NW, PD_SC, TR_SC, radius)
            n_hexes += 1.0
    happiness_percentage = 100.0 * total_happiness / n_hexes
    return [happiness_percentage, total_happiness, n_hexes]

def check_equal_neighbour_and_edge_status(col, row, hex_map, no_equal_radius=2):
    n_cols = len(hex_map)
    n_rows = len(hex_map[0])
    is_edgy = False
    has_equal_neighbour = False
    for R in range(1, no_equal_radius + 1):
        if R > 1 and hex_map[col][row] == "Ga":
            break
        neighbours = get_hexes_at_radius(col, row, R)
        for coords in neighbours:
            if coords[0] < 0 or coords[1] < 0:
                if R == 1:
                    is_edgy = True
                continue  # in case we are outside the map
            if coords[0] >= n_cols or coords[1] >= n_rows:
                if R == 1:
                    is_edgy = True
                continue  # in case we are at the end of a col/row
            if hex_map[col][row] == hex_map[coords[0]][coords[1]]:
                has_equal_neighbour = True
                break
            if R == 1 and hex_map[coords[0]][coords[1]] is None:
                is_edgy = True
            if has_equal_neighbour and is_edgy:
                return [has_equal_neighbour, is_edgy]
    return [has_equal_neighbour, is_edgy]


class Map(object):
    def __init__(self, num_players, random=True, keep_core_sectors=False, disable_6_as_centre_in_2p=False, use_323_layout=False):
        """
        2-player: 2-3-2, hex 1, 2, 3, 4, 5_,6_,7_ (option: 6_ not in centre)
        3- and 4-player: 3-4-3, hex 1, 2, 3, 4, 5, 6, 7, 8, 9, 10

        centre (x, y) - (hor, ver)

        self.map: Sector objects
        self.map_data: Tupple with sector number and rotation
        """

        self.num_players = num_players
        self.random = random
        self.width = 23
        self.height = 30
        self.keep_core_sectors = keep_core_sectors
        self.disable_6_as_centre_in_2p = disable_6_as_centre_in_2p
        self.use_323_layout = use_323_layout
        self.max_rejected_rotations = 1000000

        self.image_location = "images/"
        self.image_name = "Gaia_map"
        self.image_format = ".png"

        self.map_picture = None
        self.sector_image_width = 1884
        self.sector_image_height = 2042

        self.clockwise = True
        self.method = 0

        self.debug_level = 0

        #parameters used to eliminate illegal maps after rotation,
        #if these requirements are not met the rotation will continue
        self.minimal_equal_range = 3 #minimum range between equal planets (except Gaia and Transdim)
        self.maximum_cluster_size = 5 #set to 10 to ignore cluster size
        self.maximum_edge_planets = 3 #max number of edge planets allowed for a planet type

        self.map = None
        self.set_map()
        self.generate_full_map()

        #general parameters used in optimizations
        self.try_count = 100
        self.search_radius = 2
        self.best_balance = 0.0
        self.reset_best_map_value()
        self.best_map_data = self.get_printable_map_data()
        self.rejected_maps = 0

        # parameters used in the happiness calculation v0:
        self.range_factor = [1.0, 1.0/6.0, 1.0/12.0, 1.0/18.0]
        self.terraform_param = [2.0, 1.0, 1.0, 1.0]
        self.gaia_param = 2.0
        self.trans_param = 1.0

        # parameters used in optimization v1:
        self.NW = 0.5     # 1.0: only planet density (PD), 0.0: only Type Ratio (TR)
        self.PD_SC = 40.0
        self.TR_SC = 7.0

    def set_map(self):
        Small = ["1", "5_", "2", "3", "6_", "4", "7_"]
        Medium = ["7", "1", "5", "2", "3", "8", "4", "6", "9", "10"]
        Large = ["10", "1", "5", "9", "2", "3", "6", "8", "4", "7"]
        index = 0
        # default_sector_rotation = 0

        if self.num_players == 2:
            print "Setting up 2-3-2 map for 2 players"
            self.map = [["A", "B"], ["C", "D", "E"], ["F", "G"]]
            self.centre = [[(6, 6), (11, 7)], [(3, 13), (8, 14), (13, 15)], [(5, 21), (10, 22)]]
            if self.random:
                if not self.keep_core_sectors:
                    random.shuffle(Small)
                    if self.disable_6_as_centre_in_2p and Small[3] == "6_":
                        centre = Small[0]
                        Small[0] = Small[3]
                        Small[3] = centre
                else:
                    reminding_sectors = ["5_", "6_", "7_"]
                    random.shuffle(reminding_sectors)
                    reminding_on_the_right = random.randint(0, 1)
                    if reminding_on_the_right == 1:
                        Small[1] = reminding_sectors[0]
                        Small[4] = reminding_sectors[1]
                        Small[6] = reminding_sectors[2]
                    else:
                        #shift core sectors to the right
                        Small[1] = Small[0]
                        Small[4] = Small[3]
                        Small[3] = Small[2]
                        Small[6] = Small[5]
                        Small[0] = reminding_sectors[0]
                        Small[2] = reminding_sectors[1]
                        Small[5] = reminding_sectors[2]

            self.content = Small
        elif self.use_323_layout:
            print "Setting up 3-2-3 map for 3 players"
            self.map = [["A", "B", "C"], ["D", "E"], ["F", "G", "H"]]
            self.centre = [[(6, 6), (11, 7), (16, 8)], [(8, 14), (13, 15)],
                           [(5, 21), (10, 22), (15, 23)]]
            if self.random:
                if not self.keep_core_sectors:
                    random.shuffle(Medium)
                else:
                    reminding_sectors = ["5", "6", "7", "8", "9", "10"]
                    random.shuffle(reminding_sectors)
                    Medium[0] = reminding_sectors[0]
                    Medium[2] = reminding_sectors[1]
                    Medium[5] = reminding_sectors[2]
                    Medium[7] = reminding_sectors[3]
            self.content = Medium
        else:
            print "Setting up 3-4-3 map for 3/4 players"
            self.map = [["A", "B", "C"], ["D", "E", "F", "G"], ["H", "I", "J"]]
            self.centre = [[(6, 6), (11, 7), (16, 8)], [(3, 13), (8, 14), (13, 15), (18, 16)],
                           [(5, 21), (10, 22), (15, 23)]]
            if self.random:
                if not self.keep_core_sectors:
                    random.shuffle(Large)
                else:
                    reminding_sectors = ["5", "6", "7", "8", "9", "10"]
                    random.shuffle(reminding_sectors)
                    Large[0] = reminding_sectors[0]
                    Large[2] = reminding_sectors[1]
                    Large[3] = reminding_sectors[2]
                    Large[6] = reminding_sectors[3]
                    Large[7] = reminding_sectors[4]
                    Large[9] = reminding_sectors[5]
            self.content = Large

        for j, row in enumerate(self.map):
            for i, item in enumerate(row):
                sector_number = self.content[index]
                sector_content = Sector_data[sector_number]
                self.map[j][i] = Sector(sector_content, sector_number)
                index += 1

    def generate_full_map(self):
        """
        Resets the full map, then distributes the sectors
        """
        self.full_map = [[None for i in range(self.height)] for j in range(self.width)]
        for j, row in enumerate(self.map):
            for i, sector in enumerate(row):
                content = sector.get_content()
                position = self.centre[j][i]
                # rel_coor = sector.get_relative_coord()

                for radii, planet_list in enumerate(content):
                    planet_coord_list = get_hexes_at_radius(position[0], position[1], radii)
                    for number, hexagon in enumerate(planet_list):
                        self.full_map[planet_coord_list[number][0]][planet_coord_list[number][1]] = hexagon

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

    def set_map_by_map_data(self, map_data):
        for j, row in enumerate(self.map):
            for i, sector in enumerate(row):
                sector_rotation = map_data[j][i][1]
                while sector.get_rotation_deg() != sector_rotation:
                    sector.rotate_sector_once()
        self.generate_full_map()

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
        print sector_list


        max_row_width = len(sector_list[0])
        for i in range(1,3):
            if len(sector_list[i]) > max_row_width:
                max_row_width = len(sector_list[i])


        map_image_width = int(self.sector_image_width * max_row_width * 4.82 / 5.0)
        if self.use_323_layout:
            map_image_width = int(self.sector_image_width * max_row_width * 1.04)
        map_image_height = int(self.sector_image_height * 2.8)

        self.map_picture = Image.new("RGB", (map_image_width, map_image_height), (255, 255, 255))

        height_adjustment = int(self.sector_image_height * 0.1)
        v_scale = 0.71
        h_scale = 0.945

        sector_start_horizontal = int(self.sector_image_width * 0.56)
        sector_start_vertical = 0

        v_offsets = [0, 0, int(self.sector_image_height * 0.1)]
        h_offsets = [sector_start_horizontal, 0, sector_start_horizontal - int(self.sector_image_width * 0.18)]

        if self.use_323_layout:
            h_offsets = [self.sector_image_width * 0.18,
                         sector_start_horizontal,
                         0.0]
            v_offsets = [0,
                         int(self.sector_image_height * 0.1),
                         int(self.sector_image_height * 0.1)]

        for j, row in enumerate(sector_list):
            for i, (sector_number, sector_rotation) in enumerate(row):
                filename = self.image_location + sector_number + self.image_format
                hor = int(h_offsets[j]) + int(self.sector_image_width * h_scale * i)
                ver = int(v_offsets[j]) + (int(self.sector_image_height * v_scale * j)) + int(sector_start_vertical + height_adjustment * i)
                image = Image.open(filename)
                image = image.rotate(-sector_rotation)
                self.map_picture.paste(image, (hor, ver), image)

    def show_image_map(self):
        self.make_image_map(self.clockwise)
        self.map_picture.show()

    def set_image_name(self, image_name_without_type):
        self.image_name = image_name_without_type

    def save_image_map(self):
        self.make_image_map(self.clockwise)
        address = self.image_location + self.image_name + self.image_format
        self.map_picture.save(address)

    def rotate_map_randomly(self, abort_received_func=None):
        do_rotate = 1
        n_iter = 0
        core_sectors = ["1", "2", "3", "4"]
        while do_rotate == 1 and n_iter < self.max_rejected_rotations:
            if abort_received_func is not None:
                do_abort = abort_received_func()
                if do_abort:
                    print "ABORT!"
                    break
            for row in self.map:
                for sector in row:
                    if self.keep_core_sectors and sector.get_id() in core_sectors:
                        continue
                    n_rot = random.randint(0, 5)
                    sector.rotate_sector(n_rot)
            self.generate_full_map()
            map_valid = self.is_valid_map()
            if not map_valid:
                n_iter += 1
                continue
            '''
            if has_equal_neigbours(self.full_map, self.minimal_equal_range - 1) == 1:
                n_iter += 1
                continue
            if self.maximum_cluster_size > 9:
                break
            cluster_sizes = get_cluster_size_list(self.full_map)
            if max(cluster_sizes) > self.maximum_cluster_size:
                n_iter += 1
                continue
            '''
            do_rotate = 0
        if self.debug_level == 1:
            print n_iter
        self.rejected_maps += n_iter

    def is_valid_map(self):
        """
        Function that checks various validity parameters for a map
        This is a merged version of other such functions that was defined earliser
        Merged them so that we have to iterate through the map fewer times
        """
        planet_type_edge_count = {"Br": 0,
                                  "Bk": 0,
                                  "Ye": 0,
                                  "Re": 0,
                                  "Or": 0,
                                  "Bl": 0,
                                  "Wh": 0}

        n_cols = len(self.full_map)
        if n_cols < 1:
            return False
        n_rows = len(self.full_map[0])
        if n_rows < 1:
            return False
        ignored_types = [None, "Em"]
        cluster_sizes = []
        n_clusters = 0
        visited = [[0 for x in range(n_rows)] for y in range(n_cols)]
        for col in range(n_cols):
            for row in range(n_rows):
                if self.full_map[col][row] in ignored_types:
                    visited[col][row] = 1
                    continue
                if visited[col][row] == 1:
                    continue

                # at this point we are at a planet in a hex that has not already been visited
                # it is the start of a new cluster
                n_clusters += 1
                cluster_sizes.append(0)
                cluster_planets = [[col, row]]
                planet_index = 0
                while planet_index < len(cluster_planets):
                    planet_col = cluster_planets[planet_index][0]
                    planet_row = cluster_planets[planet_index][1]
                    planet_index += 1
                    if visited[planet_col][planet_row] == 1:
                        # need to check this here since it might have been visited after it was added to cluster_planets
                        continue

                    # at a new planet, cluster grows:
                    cluster_sizes[n_clusters - 1] += 1
                    visited[planet_col][planet_row] = 1

                    if cluster_sizes[n_clusters - 1] > self.maximum_cluster_size:
                        if self.debug_level == 2:
                            print "invalid map, cluster size >= ", self.maximum_cluster_size + 1
                        return False

                    # check if planet has equal neighbour inside max range, or is an edge planet:
                    if self.full_map[planet_col][planet_row] != "Tr":
                        planet_data = check_equal_neighbour_and_edge_status(planet_col,
                                                                            planet_row,
                                                                            self.full_map,
                                                                            self.minimal_equal_range - 1)
                        if planet_data[0]:  # it has equal neighbour
                            if self.debug_level == 2:
                                print "invalid map, has equal neighbour ", self.full_map[planet_col][planet_row]
                            return False
                        if planet_data[1]:  # it is an edge planet
                            planet_type_edge_count[self.full_map[planet_col][planet_row]] += 1
                            if planet_type_edge_count[self.full_map[planet_col][planet_row]] > self.maximum_edge_planets:
                                if self.debug_level == 2:
                                    print "invalid map, edge planets ",self.full_map[planet_col][planet_row],planet_type_edge_count
                                return False

                    # check outwards for neighbour planets:
                    neighbour_hexes = get_hexes_at_radius(planet_col, planet_row, 1)
                    for hex_id in range(6):
                        neighbour_col = neighbour_hexes[hex_id][0]
                        neighbour_row = neighbour_hexes[hex_id][1]
                        if neighbour_col < 0 or neighbour_row < 0:
                            continue  # in case we are outside the map
                        if neighbour_col >= n_cols or neighbour_col >= n_rows:
                            continue  # in case we are at the end of a col/row
                        if (visited[neighbour_col][neighbour_row] == 1)\
                                or (self.full_map[neighbour_col][neighbour_row] in ignored_types):
                            # ignore neighbour hex if it has been visited already or if it has an ignorable type of content
                            continue
                        cluster_planets.append(neighbour_hexes[hex_id])
        #if max(planet_type_edge_count) > self.maximum_edge_planets:
        #    return False
        #if max(cluster_sizes) > self.maximum_cluster_size:
        #    return False
        if self.debug_level >= 2:
            print "VALID MAP !!!! ", len(cluster_sizes)
        return True

    def set_debug_level(self, debug_level):
        self.debug_level = debug_level

    def set_method(self, method):
        self.method = method
        self.reset_best_map_value()

    def set_try_count(self, try_count):
        self.try_count = try_count

    def set_search_radius(self, search_radius):
        self.search_radius = search_radius

    def set_minimum_equal_range(self, min_equal_range):
        self.minimal_equal_range = min_equal_range

    def set_max_cluster_size(self, cluster_size):
        self.maximum_cluster_size = cluster_size

    def set_max_edge_planets(self, max_edge_planets):
        self.maximum_edge_planets = max_edge_planets

    def set_method_0_params(self, terraform_param, gaia_param, trans_param, range_factor):
        self.range_factor = range_factor
        self.terraform_param = terraform_param
        self.gaia_param = gaia_param
        self.trans_param = trans_param

    def set_method_1_params(self, NW, PD_SC, TR_SC):
        self.NW = NW
        self.PD_SC = PD_SC
        self.TR_SC = TR_SC

    def calculate_balance(self, print_happiness=0):
        if self.method == 0:
            '''Optimize for Each planet type to have neighbours it likes'''
            planet_happiness = [0.0] * 7
            for i in range(7):
                planet_happiness[i] = calc_happiness(color_wheel[i],
                                                     self.full_map,
                                                     self.gaia_param,
                                                     self.trans_param,
                                                     self.terraform_param,
                                                     self.search_radius,
                                                     self.range_factor)
            stats = get_stats(planet_happiness)
            if print_happiness != 0:
                print "Color Happiness:"
                for i in range(7):
                    if color_wheel[i] == "Bk":
                        print " Grey   - {:04.2f}".format(planet_happiness[i])
                    if color_wheel[i] == "Br":
                        print " Brown  - {:04.2f}".format(planet_happiness[i])
                    if color_wheel[i] == "Ye":
                        print " Yellow - {:04.2f}".format(planet_happiness[i])
                    if color_wheel[i] == "Or":
                        print " Orange - {:04.2f}".format(planet_happiness[i])
                    if color_wheel[i] == "Re":
                        print " Red    - {:04.2f}".format(planet_happiness[i])
                    if color_wheel[i] == "Bl":
                        print " Blue   - {:04.2f}".format(planet_happiness[i])
                    if color_wheel[i] == "Wh":
                        print " White  - {:04.2f}".format(planet_happiness[i])
                stat_string = "Stats: "
                for i in range(4):
                    if i == 0:
                        stat_string += "Avg = {:04.2f}".format(stats[i])
                    if i == 1:
                        stat_string += ", Var = {:04.3f}".format(stats[i])
                    if i == 2:
                        stat_string += ", Min = {:04.2f}".format(stats[i])
                    if i == 3:
                        stat_string += ", Max = {:04.2f}".format(stats[i])
                print stat_string
            return stats[1]
        if self.method == 1:
            '''Optimize for even distribution of planets/planet types'''
            hp = calc_map_happiness(self.full_map, self.NW, self.PD_SC, self.TR_SC, self.search_radius)[0]
            if print_happiness != 0:
                print "Happiness = {:04.2f}".format(hp)
            return hp
        if self.method == 2:
            '''Optimize for big clusters!'''
            cluster_sizes = get_cluster_size_list(self.full_map)
            stats = get_stats(cluster_sizes)
            avg_size = stats[0]
            if print_happiness != 0:
                print cluster_sizes
                print stats
            return avg_size
        if self.method == 3:
            '''Optimize for bigger largest cluster'''
            cluster_sizes = get_cluster_size_list(self.full_map)
            stats = get_stats(cluster_sizes)
            largest_size = stats[3]
            if print_happiness != 0:
                print cluster_sizes
                print stats
            return largest_size

    def is_better_balance(self, balance):
        '''
        For the various optimization methods this tells if bigger or smaller is better
        '''
        smaller_is_better = [0]
        bigger_is_better = [1, 2, 3]
        if self.method in smaller_is_better:
            return balance < self.best_balance
        elif self.method in bigger_is_better:
            return balance > self.best_balance

    def balance_map(self, print_progress_func=None, break_received_func=None):
        self.reset_best_map_value()
        self.best_map_data = self.get_printable_map_data()
        progress = 0
        progress_jump = 100
        if self.try_count >= 10:
            progress_jump = 10
        if self.try_count >= 100:
            progress_jump = 1
        print_progress_func(progress, self.best_balance, self.rejected_maps)
        for try_no in range(self.try_count):
            if break_received_func is not None:
                do_break = break_received_func()
                if do_break:
                    if print_progress_func is not None:
                        print_progress_func(100, self.best_balance, self.rejected_maps)
                    break;
            self.rotate_map_randomly(break_received_func)
            #print "rejected map count:", self.rejected_maps
            balance = self.calculate_balance()
            if self.is_better_balance(balance):
                self.best_balance = balance
                self.best_map_data = self.get_printable_map_data()
            if try_no % (self.try_count / (int(100/progress_jump))) == 0:
                progress += progress_jump
                if print_progress_func is not None:
                    print_progress_func(progress, self.best_balance, self.rejected_maps)

    def get_best_map_data(self):
        return self.best_map_data

    def set_to_balanced_map(self):
        self.set_map_by_map_data(self.best_map_data)

    def reset_best_map_value(self):
        if self.is_better_balance(-1.0):
            self.best_balance = 10000.0
        else:
            self.best_balance = 0.0
        self.rejected_maps = 0


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

def print_progress(progress, balance):
    print "progress = ", progress, ", balance = ", balance

if __name__ == "__main__":
    test_map = Map(2, True, False, False, False)
    test_map.set_method(0)
    test_map.set_debug_level(0)
    test_map.set_try_count(10)
    test_map.set_search_radius(2)
    test_map.set_max_cluster_size(9)
    test_map.set_minimum_equal_range(4)
    test_map.set_max_edge_planets(2)

    #method 0 params:
    terra_param = [1.0, 1.0, 0.1, 0.8]
    gaia_param = 1.0
    trans_param = 0.5
    range_factor = [1.0, 1.0, 0.6, 0.05]
    test_map.set_method_0_params(terra_param, gaia_param, trans_param, range_factor)

    do_loop = 2
    if do_loop == 1:
        for i in range(16, 21):
            print "Balancing map " + str(i)+"..."
            test_map.balance_map()
            print "Balance finished, best map have following data:"
            test_map.set_to_balanced_map()
            test_map.calculate_balance(1)
            print "Saving image...\n"
            if i < 10:
                test_map.set_image_name("map0"+str(i))
            else:
                test_map.set_image_name("map" + str(i))
            test_map.save_image_map()
    elif do_loop == 2:
        test_map.balance_map()#print_progress)
        test_map.set_to_balanced_map()
        test_map.is_valid_map()
        #test_map.calculate_balance(1)
        #print "Saving image...\n"
        #test_map.set_image_name("test_map")
        #test_map.save_image_map()
        test_map.show_image_map()
    else:
        test_map.calculate_balance(1)

    #test_map.show_image_map()
    #hex_map = test_map.get_full_map()
    #print has_equal_neigbours(hex_map)

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
    #clusters = get_cluster_size_list(hex_map)
    #print max(clusters)
    #clusters.sort()
    #print clusters

