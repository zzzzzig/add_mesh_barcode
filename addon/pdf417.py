# Uses pdf417gen to generate PDF417 Barcodes in Blender

import bpy
# import bmesh
# from math import radians
import numpy
# from bpy_extras import object_utils
from .. generators.pdf417gen import encode  # , render_svg, render_image
from .. generators.pdf417gen.rendering import modules, barcode_size

from . shared import resize_along_axis
from . shared import move_origin_3d_cursor, center_on_cursor
from . shared import build_borders, build_obj_from_table


class ABC_OT_mesh_pdf417(bpy.types.Operator):
    """Construct a QR code mesh"""
    bl_idname = "abc.make_pdf417"
    bl_label = "PDF417 Code"
    bl_options = {'REGISTER', 'UNDO'}

    data: bpy.props.StringProperty(
        name="Data",
        description="Data to store in the PDF417 code",
        default="text")
    columns: bpy.props.IntProperty(
        name="Columns",
        description="Sets the number of columns in which to store the data. "
                    "Add more for more data storage. No 'correct' ammount. "
                    "Play with it until it looks the way you want it to."
                    "1-30, Default 1",
        default=1, min=1, max=30)
    security: bpy.props.IntProperty(
        name="Security",
        description="Sets the error correction level. "
                    "Generates a bigger code but can survive more damage. "
                    "Will probably require more columns at higher levels",
        default=0, min=0, max=8)
    invert: bpy.props.BoolProperty(
        name="Invert",
        description="Create mesh in the dark areas instead of light"
                    " The big blocks near the ends should be dark",
        default=False)
    border: bpy.props.IntProperty(
        name="Border",
        description="Border width to maintain quiet space around code. "
                    "PDF417 codes need a blank space around them in order to be read. "
                    "(disabled when inverted)",
        default=2, min=0, max=10)
    join: bpy.props.BoolProperty(
        name="Join blocks",
        description="Join vertices of adjacent blocks. Same as merge vertices by distance or remove doubles",
        default=True)
    rescale: bpy.props.BoolProperty(
        name="Rescale",
        description="Scale the code to specific size on the chosen axis",
        default=True)
    rescale_axis: bpy.props.EnumProperty(
        items=[('X', "X (default)", "Scale along X"),
               ('Y', "Y", "Scale along Y")],  # ('Z', "Z", "Scale along Z")]
        name="Resize axis",
        description="Choose axis to rescale along to the specified length",
        default='X')
    size: bpy.props.FloatProperty(
        name="Axis length",
        description="Specify length of chosen axis",
        default=1, min=0)
    ratio: bpy.props.FloatProperty(
        name="Ratio",
        description="Specify the module height ratio. "
                    "PDF417 modules are tall and narrow. "
                    "They can still be read at different ratios, "
                    "but it's not reliable. (Default:3)",
        default=3, min=0)
    center: bpy.props.BoolProperty(
        name="Center on cursor",
        description="Centers the generated code on the 3D cursor.",
        default=False)

    def create_pdf_table(self):
        codes = encode(self.data,
                       columns=self.columns,
                       security_level=self.security)

        width, height = barcode_size(codes)
        table = numpy.full((height, width), False)

        for col_id, row_id, visible in modules(codes):
            table[row_id][col_id] = visible

        return table



    def execute(self, context):

        # pdf_table = self.create_pdf_table()

        # self.report({'INFO', 'OPERATOR'}, 'test report')

        try:
            pdf_table = self.create_pdf_table()
        except ValueError as ex:
            error_report = "\n".join(ex.args)
            print(str(ex))
            self.report({'ERROR'}, str(ex))
            return {'CANCELLED'}


        if not self.invert:
            pdf_table = build_borders(pdf_table, self.border, self.ratio)

        pdf_obj = build_obj_from_table(
            context,
            pdf_table,
            self.ratio,
            self.invert,
            self.join,
            name="PDF417Code")

        # optionally rescales the QR code object
        if self.rescale:
            resize_along_axis(pdf_obj, self.size, self.rescale_axis)

        # optionally centers the object on the 3D cursor
        if self.center:
            center_on_cursor(pdf_obj)
        else:
            move_origin_3d_cursor(pdf_obj)

        return {'FINISHED'}
