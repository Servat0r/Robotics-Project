from .povwriter import *
import numpy as np


# Calcolo posizione camere pneumatiche usando matrice rotazione, posizione locale
# e posizione globale centroide sezione
def pos_cam_in_cross_section(theta, delta):
    # Calcola posizione locale attuatore nella sezione trasversale
    x = delta * np.cos(np.radians(theta))
    y = delta * np.sin(np.radians(theta))
    z = 0
    r = np.array([x, y, z])

    return r


class ChamberPOV:

    def __init__(self, geometric, visual):
        # geometric
        self.n_elems = geometric['n_elems']
        self.theta = geometric['theta']
        self.delta = geometric['delta']
        self.radii_cam = geometric['radius'] * np.ones(self.n_elems)
        self.tops_pos = geometric['centerline_tops']
        self.bots_pos = geometric['centerline_bots']
        self.directors = geometric['centerline_directors']

        self.r_local = pos_cam_in_cross_section(theta=self.theta, delta=self.delta)
        self.tops_cam, self.bots_cam = self.get_global_actuator_positions()

        # Convert from xyz to xzy (POV-ray) - after all the computations
        self.tops_cam = self.tops_cam[:, :, [0, 2, 1]]
        self.bots_cam = self.bots_cam[:, :, [0, 2, 1]]

        # visual
        # TODO: chamber visuals are static for now
        self.rgb = visual['rgb']
        self.transmit = visual['transmit']
        self.ambient = visual['ambient']
        self.phong = visual['phong']

    def get_global_actuator_positions(self):
        time = self.tops_pos.shape[0]
        tops_cam = np.empty(shape=(time, self.n_elems, 3))
        bots_cam = np.empty(shape=(time, self.n_elems, 3))

        for t, (directors_t, tops_t, bots_t) in enumerate(zip(self.directors, self.tops_pos, self.bots_pos)):  # per ogni t
            for s, (director_s, top_s, bot_s) in enumerate(zip(directors_t, tops_t, bots_t)):  # per ogni s
                tops_cam[t, s] = np.dot(director_s.T, self.r_local) + top_s
                bots_cam[t, s] = np.dot(director_s.T, self.r_local) + bot_s

        return tops_cam, bots_cam

    def to_pov(self, pov_file, t):
        RodElems(pov_file, self.tops_cam[t], self.bots_cam[t], self.radii_cam,
                 rgb=self.rgb, transmit=self.transmit,
                 ambient=self.ambient, phong=self.phong)
