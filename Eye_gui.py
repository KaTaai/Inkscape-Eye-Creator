#! /usr/bin/python
'''
Create an eye using circles in Inkscape
'''
from math import sqrt,cos, sin, pi, pow

import inkex
from inkex import GenerateExtension
from inkex import Circle

def calculateEyeRadius(height, iris_width, crescent_factor, shape):
    if shape=="Lens":
        radius=(pow(height,2)+pow((iris_width/2),2))/(2*(iris_width/2))
        return (radius,radius)
    else:
        r2 = (pow(height,2)+pow((iris_width),2))/(2*(iris_width))
        r3 = (pow(height,2)+pow((iris_width*crescent_factor),2))/(2*(iris_width*crescent_factor))
        # raise ValueError(f"Circle 1 {r2}, Circle 2 {r3}, Height {height}, Iris width {iris_width}, Shape {shape}")
        return (r2,r3)

def rotate(radius, angle):
    return {"x":cos(angle/180*pi)*radius, "y":sin(angle/180*pi)*radius}

def interCircleDistance(iris_width, offset, iris_radiuses, stroke_w_eye, crescent_factor, shape):
    if shape=="Lens":
        d2 = iris_width/2-(iris_radiuses[0]-(stroke_w_eye/2))+offset
        d3 = -1*(iris_width/2-(iris_radiuses[1]-(stroke_w_eye/2)))+offset
        distance = (d2,d3)
    else:
        d2 = iris_width-(iris_radiuses[0]-(stroke_w_eye/2))+offset
        d3 = iris_width*crescent_factor-(iris_radiuses[1]-(stroke_w_eye/2))+offset
        distance = (d2,d3)
        # the second one is larger
    return distance

def heightCalculator(main_circle_radius, offset):
    return sqrt(pow(main_circle_radius,2)-pow(offset,2))

class Eye(GenerateExtension):
    def __init__(self):
        GenerateExtension.__init__(self)
        
        self.arg_parser.add_argument("-d", "--d-main",
                        action="store", type=float,
                        dest="diameter", default=25.000,
                        help="The diameter of the main circle")
        self.arg_parser.add_argument("--iris-width",
                        action="store", type=float,
                        dest="iris_width", default=5.000,
                        help="The width of the iris")
        self.arg_parser.add_argument("-m", "--stroke-w-main",
                        action="store", type=float,
                        dest="stroke_w_main", default=0.500,
                        help="The width of the stroke on the main circle")
        self.arg_parser.add_argument("-e", "--stroke-w-eye",
                        action="store", type=float,
                        dest="stroke_w_eye", default=0.500,
                        help="The width of the stroke on the iris circles")
        self.arg_parser.add_argument("-a", "--angle",
                        action="store", type=float,
                        dest="angle", default=0.000,
                        help="The angle change of the final figure")
        self.arg_parser.add_argument("--shape",
                        action="store", type=str,
                        dest="shape", default="Lens",
                        help="The shape of the iris")
        self.arg_parser.add_argument("--offset",
                        action="store", type=float,
                        dest="offset", default="0",
                        help="Offset of the top of the iris")
        self.arg_parser.add_argument("--crescent-factor",
                        action="store", type=float,
                        dest="crescent_factor", default="0.5",
                        help="Offset of the top of the iris")
        # self.arg_parser.add_argument("-y", "--y-origin-main",
        #                 action="store", type=float,
        #                 dest="y_origin", default=0.0,
        #                 help="The y-origin of the main circle")
        # self.OptionParser.add_option("", "", action="store", type=float, dest="", default=25, help="")

    def generate(self): #pylint: disable=no-member
        so=self.options

        corrected_main_circle_radius = (so.diameter-so.stroke_w_main)/2
        if so.offset>=corrected_main_circle_radius or so.offset<=-1*corrected_main_circle_radius:
            # the offset ends up outside the main circle
            # Throw some error
            raise ValueError(f"The offset pushes the tops of the iris outside the main circle. Bring it to between {-1*corrected_main_circle_radius} and {corrected_main_circle_radius} for the current settings.")
        
        main_circle = Circle(cx="0", cy="0")
        main_circle.set("r", str(corrected_main_circle_radius))
        main_circle.set("style",f"fill:none;stroke:#ff0000;stroke-width:{str(so.stroke_w_main)};")
        
        requiredHeight = heightCalculator(corrected_main_circle_radius, so.offset)
        irisRadiuses = calculateEyeRadius(requiredHeight, so.iris_width, so.crescent_factor, so.shape)
        inter_circle_distance = interCircleDistance(so.iris_width, so.offset, irisRadiuses, so.stroke_w_eye, so.crescent_factor, so.shape)
        # so.iris_width/2-(irisRadiuses[0]-(so.stroke_w_eye/2))

        LC_coords = rotate(inter_circle_distance[0],so.angle)
        Left_circle = Circle(cx=str(LC_coords["x"]), cy=str(LC_coords["y"]))
        Left_circle.set("r", str(irisRadiuses[0]-(so.stroke_w_eye/2)))
        Left_circle.set("style",f"fill:none;stroke:#000000;stroke-width:{str(so.stroke_w_eye)};")

        RC_coords = rotate(inter_circle_distance[1],so.angle)
        Right_circle = Circle(cx=str(RC_coords["x"]), cy=str(RC_coords["y"]))
        Right_circle.set("r", str(irisRadiuses[1]-(so.stroke_w_eye/2)))
        Right_circle.set("style",f"fill:none;stroke:#000000;stroke-width:{str(so.stroke_w_eye)};")

        yield main_circle
        yield Left_circle
        yield Right_circle
    #     # raise inkex.AbortExtension(message="This is a test")
    #     # print("This is a test")
    #     #examples spirograph.py in /usr/share/inkscape/extensions
    # /usr/share/inkscape/extensions/draw_from_triangle.py
    # /home/kataai/Downloads/nicechart.py
    
    # self.options
        pass
    
if __name__ == '__main__':
    e= Eye()
    e.run()