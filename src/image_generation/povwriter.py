def POVRay_Sphere(pov_file, center, radius, rgb, ambient, transmit, phong):
    pov_file.writelines("sphere {\n")
    pov_file.writelines("<%f, %f, %f>, %f\n" % (*center, radius))
    pov_file.writelines("pigment { color rgb <%f, %f, %f>  transmit %f}\n" % (*rgb, transmit))
    pov_file.writelines("finish { ambient %f phong %f}\n" % (ambient, phong))
    pov_file.writelines("}\n\n")  # end of sphere


def POVRay_Cone(pov_file, top, bot, r_top, r_bot, rgb, transmit, ambient, phong):
    pov_file.writelines("cone {\n")
    pov_file.writelines("<%f, %f, %f>, %f\n" % (*top, r_top))  # // Center of one end
    pov_file.writelines("<%f, %f, %f>, %f\n" % (*bot, r_bot))  # // Center of other end
    # pov_file.writelines("open\n")                               # // Remove end caps
    pov_file.writelines("pigment{ color rgb<%f,%f,%f>  transmit %f }\n" % (*rgb, transmit))
    pov_file.writelines("finish{ ambient %f phong %f}\n" % (ambient, phong))
    pov_file.writelines("}\n\n")


def POVRay_HollowCylinder(pov_file, top, bot, radius, inner_cavity_radius, rgb, transmit, ambient, phong):
    pov_file.writelines("difference{\n")
    # outer cylinder
    pov_file.writelines("cylinder {\n")
    pov_file.writelines("<%f, %f, %f>, <%f, %f, %f>, %f\n" % (*top, *bot, radius))  # // Center of one end
    pov_file.writelines("}\n")
    # inner cylinder
    top_inner = top + 1e-4  # solves bug
    bot_inner = bot - 1e-4
    pov_file.writelines("cylinder {\n")
    pov_file.writelines(
        "<%f, %f, %f>, <%f, %f, %f>, %f\n" % (*top_inner, *bot_inner, inner_cavity_radius))  # // Center of one end
    pov_file.writelines("}\n")
    pov_file.writelines("pigment{ color rgb<%f,%f,%f>  transmit %f }\n" % (*rgb, transmit))
    pov_file.writelines("finish{ ambient %f phong %f}\n" % (ambient, phong))
    pov_file.writelines("} // end difference\n\n")


def BottomTerminal(pov_file, top, bot, dummy_top, dummy_bot, radius, inner_cavity_radius, rgb, transmit, ambient,
                   phong):
    pov_file.writelines("difference{\n")
    # outer cylinder
    pov_file.writelines("cylinder {\n")
    pov_file.writelines("<%f, %f, %f>, <%f, %f, %f>, %f\n" % (*top, *bot, radius))  # // Center of one end
    pov_file.writelines("}\n")
    # inner cylinder
    pov_file.writelines("cylinder {\n")
    pov_file.writelines(
        "<%f, %f, %f>, <%f, %f, %f>, %f\n" % (*dummy_top, *dummy_bot, inner_cavity_radius))  # // Center of one end
    pov_file.writelines("}\n")
    pov_file.writelines("pigment{ color rgb<%f,%f,%f>  transmit %f }\n" % (*rgb, transmit))
    pov_file.writelines("finish{ ambient %f phong %f}\n" % (ambient, phong))
    pov_file.writelines("} // end difference\n\n")


def POVRay_Cylinder(pov_file, top, bot, radius, rgb, transmit, ambient, phong):
    pov_file.writelines("cylinder {\n")
    pov_file.writelines("<%f, %f, %f>, <%f, %f, %f>, %f\n" % (*top, *bot, radius))  # // Center of one end
    # pov_file.writelines("open\n")                               # // Remove end caps
    pov_file.writelines("pigment{ color rgb<%f,%f,%f>  transmit %f }\n" % (*rgb, transmit))
    pov_file.writelines("finish{ ambient %f phong %f}\n" % (ambient, phong))
    pov_file.writelines("}\n\n")


def RodElems(pov_file, tops, bots, radii, rgb, transmit, ambient, phong):
    # N segmenti
    for top, bot, radius in zip(tops, bots, radii):
        POVRay_Cylinder(pov_file, top, bot, radius, rgb, transmit, ambient, phong)
    # N-1 sfere nei nodi interni per raccordo
    # for center, radius in zip(tops[1:], radii[1:]):
    #    POVRay_Sphere(pov_file, center, radius, rgb, ambient, transmit, phong)


def Actuator(pov_file, pos, radii, directors, n_elems, rgb, transmit, ambient):
    for i in range(n_elems - 1):
        top, bot = pos[:, i], pos[:, i + 1]
        top = np.dot(directors[:, :, i], top)
        bot = np.dot(directors[:, :, i], bot)
        r_top, r_bot = radii[i], radii[i + 1]

        POVRay_Cone(pov_file, top, bot, r_top, r_bot, rgb, transmit, ambient)


def Actuator2(pov_file, tops, bots, radii, n_elems, rgb, transmit, ambient):
    for i in range(n_elems - 1):
        top, bot = tops[:, i], bots[:, i]
        r_top, r_bot = radii[i], radii[i]

        POVRay_Cone(pov_file, top, bot, r_top, r_bot, rgb, transmit, ambient)


def Rod(pov_file, pos, radii, n_elems, rgb, transmit, ambient, phong):
    for i in range(n_elems - 1):
        top, bot = pos[:, i], pos[:, i + 1]
        r_top, r_bot = radii[i], radii[i + 1]

        POVRay_Cone(pov_file, top, bot, r_top, r_bot, rgb, transmit, ambient, phong)


def RodSphereSweep(pov_file, pos, radii, n_elems, rgb, transmit, ambient, phong):
    pov_file.writelines("sphere_sweep { cubic_spline\n")
    pov_file.writelines("%d,\n" % n_elems)

    for i in range(n_elems):
        pov_file.writelines("<%f,%f,%f>, %f\n" % (pos[:, i], radii[i]))

    pov_file.writelines("pigment{ color rgb <%f,%f,%f>  transmit %f }\n" % (rgb[0], rgb[1], rgb[2], transmit))
    pov_file.writelines("finish{ ambient %f phong %f}\n" % (ambient, phong))
    pov_file.writelines("}\n\n")


def POVRay_frame(pov_file, base, frame_width, frame_length, frame_height, rgb, transmit):
    a1 = base[0] - frame_width / 2
    a2 = base[1] - frame_height / 2
    a3 = base[2] - frame_length / 2

    b1 = base[0] + frame_width / 2
    b2 = base[1] + frame_height / 2
    b3 = base[2] + frame_length / 2

    pov_file.writelines("box {\n")
    pov_file.writelines("<%f,%f,%f> \n" % (a1, a2, a3))  # // Near lower left corner
    pov_file.writelines("<%f,%f,%f> \n" % (b1, b2, b3))  # // Far upper right corner
    pov_file.writelines("texture{ Glass ")
    pov_file.writelines("pigment {color rgb<%f,%f,%f>  transmit %f }\n" % (*rgb, transmit))
    pov_file.writelines("}}\n\n")


def POVRay_HollowBox(pov_file, base, frame_width, frame_length, frame_height, border, rgb):
    a1 = base[0] - frame_width / 2
    a2 = base[1] - frame_height / 2
    a3 = base[2] - frame_length / 2

    b1 = base[0] + frame_width / 2
    b2 = base[1] + frame_height / 2
    b3 = base[2] + frame_length / 2

    c1 = base[0] - (frame_width / 2 - border)
    c2 = base[1] - frame_height / 2
    c3 = base[2] - (frame_length / 2 - border)

    d1 = base[0] + (frame_width / 2 - border)
    d2 = base[1] + frame_height / 2
    d3 = base[2] + (frame_length / 2 - border)

    pov_file.writelines("difference {\n")
    # outer box
    pov_file.writelines("box {\n")
    pov_file.writelines("<%f,%f,%f> \n" % (a1, a2, a3))  # // Near lower left corner
    pov_file.writelines("<%f,%f,%f> \n" % (b1, b2, b3))  # // Far upper right corner
    pov_file.writelines("pigment { color rgb<%f,%f,%f> }\n" % (rgb[0], rgb[1], rgb[2]))
    pov_file.writelines("}\n")
    # inner box
    pov_file.writelines("box {\n")
    pov_file.writelines("<%f,%f,%f> \n" % (c1, c2, c3))  # // Near lower left corner
    pov_file.writelines("<%f,%f,%f> \n" % (d1, d2, d3))  # // Far upper right corner
    pov_file.writelines("pigment { color rgb<%f,%f,%f> transmit 1 }\n" % (rgb[0], rgb[1], rgb[2]))
    pov_file.writelines("}\n")
    pov_file.writelines("}\n\n")


def Camera(pov_file, location, look_at, angle=30, flash=False):
    pov_file.writelines("camera {\n")
    pov_file.writelines("location <%f,%f,%f>\n" % (location))
    pov_file.writelines("look_at  <%f,%f,%f>\n" % (look_at))
    pov_file.writelines("angle %f\n" % angle)
    pov_file.writelines("}\n\n")

    if flash:
        # add camera flash
        # light_source{ Camera_Position  color rgb<0.9,0.9,1>*0.1}  // flash light
        # pov_file.writelines("light_source { <%f,%f,%f> color rgb <0.9,0.9,1> * 0.1 spotlight }\n\n" % location)
        pov_file.writelines("light_source { <%f,%f,%f> color rgb <0.9,0.9,1> * 0.1 }\n\n" % location)


def Include(pov_file, includes):
    for include in includes:
        pov_file.writelines("#include \"" + include + "\"\n")


def Light(pov_file, location, color="White"):
    pov_file.writelines("light_source { <%f,%f,%f> color %s}\n\n" % (*location, color))


def RGBLight(pov_file, location, rgb=(1, 1, 1)):
    pov_file.writelines("light_source { <%f,%f,%f> color rgb <%f,%f,%f>}\n\n" % (*location, *rgb))


def Background(pov_file, rgb):
    pov_file.writelines("background { color rgb <%f, %f, %f> }\n\n" % (rgb[0], rgb[1], rgb[2]))


def MonochromaticPlane(pov_file, plane_normal, plane_y, rgb):
    pov_file.writelines("plane { <%f,%f,%f>, %f\n" % (*plane_normal, plane_y))  # plane normal, plane y w.r.t origin
    pov_file.writelines("pigment{color rgb <%f, %f, %f> }}\n\n" % (rgb[0], rgb[1], rgb[2]))


def CheckerPlane(pov_file, plane_normal, plane_y, color1, color2):
    pov_file.writelines("plane { <%f,%f,%f>, %f\n" % (*plane_normal, plane_y))  # plane normal, plane y w.r.t origin
    pov_file.writelines("pigment { checker color %s, color %s }\n" % (color1, color2))
    pov_file.writelines("}\n\n")


def WoodPlane(pov_file, plane_normal, plane_y, pigment='Dark_Wood'):
    "Pigment options (Cherry_Wood, Dark_Wood, Tan_Wood, White_Wood)"
    pov_file.writelines("plane { <%f,%f,%f>, %f\n" % (*plane_normal, plane_y))  # plane normal, plane y w.r.t origin
    pov_file.writelines("pigment { %s }\n" % pigment)  # Cherry_Wood, Dark_Wood, Tan_Wood, White_Wood
    pov_file.writelines("}\n\n")


def Arrow(pov_file, start=None, end=None, color=None):
    pov_file.writelines("# macro Arrow (START, END)\n")  # defines the start of a macro
    # change these to suit your scale and taste these will be the common measurements of every arrow
    pov_file.writelines("# local Arrow_Head_Length = .005;\n")
    pov_file.writelines("# local Arrow_Head_Radius = .004;\n")  # large radius of cone
    pov_file.writelines("# local Arrow_Shaft_Radius = .002;\n")

    pov_file.writelines("# local Arrow_Vector = END - START;\n") # defines the direction in which the arrow is pointing
    pov_file.writelines("# local Shaft_Meets_Head = END - vnormalize (Arrow_Vector) * Arrow_Head_Length;\n")
    # vnormalize takes the direction of the arrow and makes its length equal to 1 multiplying this by the length
    # of the arrowhead and subtracting it from the end leaves room for the arrowhead

    pov_file.writelines("cylinder{START, Shaft_Meets_Head, Arrow_Shaft_Radius}\n")  # this is the shaft
    pov_file.writelines("cone{Shaft_Meets_Head, Arrow_Head_Radius, END, 0}\n")  # this is the head
    pov_file.writelines("# end\n")  # macro Arrow (START, END) /* this is the end of the macro */

    # TODO: in soft_pov.py, start = rod_tip, end=compute as in notebook (save force vector from simulation)
    #pov_file.writelines("union{Arrow( <0, -0.19, 0 >, < 0.02886751, -0.21886751, -0.02886751 >)\n")
    pov_file.writelines("union{Arrow( <%f, %f, %f>, <%f, %f, %f>)\n" % (*start, *end))
    pov_file.writelines("pigment{rgb %s}\n" % color)
    pov_file.writelines("finish{ ambient 1 }}\n")
    # call the macro inside a union statement so you can add your textures and transformations


# IGNORA
# Se abbiamo bisogno di un oggetto che sia
# completamente illuminato indipendentemente dalla situazione delle luci in una data scena, possiamo
# farlo artificialmente specificando un valore per ambient di 1 e di 0 per diffuse. Questo
# eliminerà tutte le ombre e fornirà, semplicemente, il più brillante valore di colore all'oggetto in tutti
# i suoi punti. Questo può essere utile per simulare oggetti che emettono luce come lampadine e per il
# cielo in scene dove esso non può essere adeguatamente illuminato con altri mezzi.

# filter (transparency) e transmit regolano trasparenza in modo diverso
# ambient = luce propria
# phong = luccichio