import json
import numpy as np
import sys
from tqdm import tqdm
from .povwriter import *
from .povisupport import *


"""
Generates .POV files that can be rendered.
"""


def cnn_generate_images(data_path=None, json_config=None):
    data_path = data_path if data_path is not None else \
        'C:/Users/Amministratore/PycharmProjects/RoboticsProject/data/motion/ws_0.5.npz'
    json_config = json.load(open(json_config, 'r')) if json_config and isinstance(json_config, str) else \
        {
            "rgb_terminals": [0, 0, 128],
            "background_rgb": [1, 1, 1],
            "plane": "monochromatic",
            "monochromatic_rgb": [0.2, 0.8, 0.2],
            "wood_pigment": "Dark_Wood",
            "spherical": False
        }

    print(json_config)
    data = np.load(data_path)
    print("data loaded")

    pos = data["position_rod1"]  # (time, yzx, nodi, )
    radii = data["radii_rod1"]  # (time, elems)
    directors = data["directors_rod1"]  # (time, righe, colonne, elems)
    n_elems = radii.shape[1]  # (elems)
    time = pos.shape[0]

    # Scambio assi in modo da avere (time, nodi/elems, ...)
    pos = pos.transpose(0, 2, 1)
    directors = directors.transpose(0, 3, 1, 2)

    # Scambio assi da yzx (PyElastica) a xyz per fare calcoli ragionevolmente
    # Quindi scambio le colonne dei direttori Q.
    pos = pos[:, :, [2, 0, 1]]
    directors = directors[:, :, :, [2, 0, 1]]

    """
    ARM
    """

    # Arm geometric
    # Dalle posizioni dei nodi della trave crea coppie (top,bot)
    # per delimitare i segmenti cilindrici
    tops_pos = pos[:, :-1, :]  # basi superiori dei segmenti
    bots_pos = pos[:, 1:, :]  # basi inferiori dei segmenti

    # radii
    inner_cavity_radius = 0.008

    # Arm visual
    rgb_arm = np.array([75, 83, 32]) / 255
    transmit_arm = 0.5
    ambient_arm = 0.9
    phong_arm = 1

    """
    CHAMBERS
    """

    # Chambers, Geometric
    theta_1, theta_2, theta_3 = 90, 210, 330
    delta = 0.02
    ro1 = 0.00779
    ro2 = 0.00639
    radii_cam = ro2 * np.ones(n_elems)

    # Chambers, visual
    geometric_cam1 = {'theta': theta_1,
                      'delta': delta,
                      'radius': ro2,
                      'n_elems': n_elems,
                      'centerline_tops': tops_pos,
                      'centerline_bots': bots_pos,
                      'centerline_directors': directors}

    geometric_cam2 = geometric_cam1.copy()
    geometric_cam3 = geometric_cam1.copy()
    geometric_cam2['theta'] = theta_2
    geometric_cam3['theta'] = theta_3

    visual_cam1 = {'rgb': [1, 1, 1],
                   'transmit': 0.1,
                   'ambient': 1,
                   'phong': 1}

    visual_cam2 = visual_cam1.copy()
    visual_cam3 = visual_cam1.copy()

    chamber_1 = ChamberPOV(geometric_cam1, visual_cam1)
    chamber_2 = ChamberPOV(geometric_cam2, visual_cam2)
    chamber_3 = ChamberPOV(geometric_cam3, visual_cam3)

    """
    Terminals
    """
    # Terminals, visual
    # TODO: change rgb terminals  ## OK
    rgb_terminals = np.array(json_config['rgb_terminals']) / 255.0  # NOTE: RGB values between 0 and 1.
    transmit_terminals = 0
    ambient_terminals = 1
    phong_terminals = 1

    # Top terminal, geometric
    top_top_terminal_t = np.array([0, 0, 0])   # xzy
    bot_top_terminal_t = np.array([0, 0.02, 0])  # xzy
    top_terminal_radius = radii[0, 0]

    # Bottom terminal, geometric
    height_bot_terminal = 0.005
    bots_bot_terminal = pos[:, -1, :]
    tops_bot_terminal = np.array(
        [bots_bot_terminal_t + np.dot(directors_t_last.T, np.array([0, 0, 0.005])) for directors_t_last, bots_bot_terminal_t
         in zip(directors[:, -1, :, :], bots_bot_terminal)])

    dummy_tops_bot_terminal = np.array([tops_bot_terminal_t + np.dot(directors_t_last.T, np.array([0, 0, 0.005 + 1e-4])) for
                                        directors_t_last, tops_bot_terminal_t in
                                        zip(directors[:, -1, :, :], tops_bot_terminal)])
    dummy_bots_bot_terminal = np.array(
        [bots_bot_terminal_t + np.dot(directors_t_last.T, np.array([0, 0, - 0.005 - 1e-4])) for
         directors_t_last, bots_bot_terminal_t in
         zip(directors[:, -1, :, :], bots_bot_terminal)])

    """
    Rigid frame
    """
    # Rigid frame, geometric
    frame_width = 0.3
    frame_length = 0.25
    frame_height = 0.005
    frame_center = pos[0, 0, :] + (0, 0, frame_height / 2 + 0.02)  # frame e terminal height

    # Rigid frame, visual
    rgb_frame = [0.1, 0.1, 0.1]
    transmit_frame = 0.8

    # Convert da xyz a xzy (POV-ray)
    tops_pos = tops_pos[:, :, [0, 2, 1]]
    bots_pos = bots_pos[:, :, [0, 2, 1]]
    tops_bot_terminal = tops_bot_terminal[:, [0, 2, 1]]
    bots_bot_terminal = bots_bot_terminal[:, [0, 2, 1]]
    dummy_tops_bot_terminal = dummy_tops_bot_terminal[:, [0, 2, 1]]
    dummy_bots_bot_terminal = dummy_bots_bot_terminal[:, [0, 2, 1]]
    pos_tip = pos[:, -1, [0, 2, 1]]
    frame_center = frame_center[[0, 2, 1]]

    # camera
    camera_location = (0.5, -0.15, 0)  # xzy
    camera_look_at = (0, -0.1, 0)  # xzy
    camera_angle = 60

    # lights
    rgb_light_location = (0.3, 0.05, -0.3)  # xzy
    rgb_flash = np.array([0.9, 0.9, 1]) * 0.1
    light_location = (0, 2000, 1000)  # xzy

    """
    create pov
    """

    file_dir = "./POV/"

    sampling_frequency = 100  # Hz
    rendering_frequency = sampling_frequency  # Hz (i.e. generate POV of all samples)
    frames_to_skip = int(sampling_frequency / rendering_frequency)
    time_index = np.arange(0, time, frames_to_skip)


    def write_scene(t, i):
        """
        Writes one frame in the .POV file.
        :param t: time index
        :param i: file index
        :return:
        """
        file_name = "%09d_rod.pov" % i
        pov_file = open(file_dir + file_name, "w")

        # set up scene
        Include(pov_file, includes=["colors.inc", "textures.inc", "shapes.inc", "stones.inc"])
        # TODO: change rgb of background ## OK
        Background(pov_file, rgb=tuple(json_config['background_rgb']))
        Camera(pov_file, location=camera_location, look_at=camera_look_at, angle=camera_angle, flash=True)
        RGBLight(pov_file, location=rgb_light_location, rgb=rgb_flash)  # luce addizionale da camera
        Light(pov_file, location=light_location, color="White")

        # TODO: choose plane (uncomment/comment, choose colors/pigment) ## OK
        # NB: it works also without plane
        plane = json_config.get('plane', None)
        if plane == 'monochromatic':
            MonochromaticPlane(pov_file, plane_normal=(0, 1, 0), plane_y=-1, rgb=tuple(json_config['monochromatic_rgb']))
        elif plane in ['checker', 'checkers']:
            CheckerPlane(pov_file, plane_normal=(0, 1, 0), plane_y=-1, color1='White', color2='Black')
        elif plane == 'wood':
            WoodPlane(pov_file, plane_normal=(0, 1, 0), plane_y=-1, pigment=json_config['wood_pigment'])
            # Pigment options (Cherry_Wood, Dark_Wood, Tan_Wood, White_Wood)

        # Arm body
        RodElems(pov_file, tops_pos[t], bots_pos[t], radii[t],
                 rgb=rgb_arm, transmit=transmit_arm, ambient=ambient_arm, phong=phong_arm)

        # Actuators
        chamber_1.to_pov(pov_file, t)
        chamber_2.to_pov(pov_file, t)
        chamber_3.to_pov(pov_file, t)

        # Bottom terminal
        BottomTerminal(pov_file,
                       tops_bot_terminal[t], bots_bot_terminal[t],
                       dummy_tops_bot_terminal[t], dummy_bots_bot_terminal[t],
                       radius=radii[t, -1], inner_cavity_radius=inner_cavity_radius,
                       rgb=rgb_terminals, transmit=transmit_terminals, ambient=ambient_terminals, phong=phong_terminals)

        # Top Terminal
        POVRay_HollowCylinder(pov_file, top_top_terminal_t, bot_top_terminal_t, top_terminal_radius,
                              inner_cavity_radius=inner_cavity_radius,
                              rgb=rgb_terminals, transmit=transmit_terminals, ambient=ambient_terminals,
                              phong=phong_terminals)

        # Rigid frame
        POVRay_frame(pov_file, frame_center, frame_width, frame_length, frame_height,
                     rgb=rgb_frame, transmit=transmit_frame)

        # Objects
        # TODO: add spherical objects (positions xzy) that may partially occlude the robot.
        # comment/uncomment, change centre, radius, rgb.
        if json_config['spherical']:
            POVRay_Sphere(pov_file, center=(0.1, -0.2, 0.1), radius=0.05, rgb=(1,0,0), ambient=1, transmit=0, phong=1)

        pov_file.close()

    # write all frames
    for file_index, time_index in enumerate(tqdm(time_index)):
        write_scene(t=time_index, i=file_index)


if __name__ == "__main__":
    cnn_generate_images(
        sys.argv[1] if len(sys.argv) > 1 else None,
        sys.argv[2] if len(sys.argv) > 2 else None,
    )

