'''Uses aztec_code_generator to generate Aztec Barcodes in Blender'''

import bpy
import bmesh
# from math import radians
import numpy
from bpy_extras import object_utils

from .. generators.aztec.aztec_code_generator import AztecCode

from . shared import resize_along_axis
from . shared import move_origin_3d_cursor, center_on_cursor
from . shared import build_borders, build_obj_from_table


# referance usage code
'''
data = 'Aztec Code 2D :)'
aztec_code = AztecCode(data)
aztec_code.save('aztec_code.png', module_size=4)

data = 'Aztec Code 2D :)'
aztec_code = AztecCode(data)
aztec_code.print_out()
'''


class ABC_OT_mesh_aztec(bpy.types.Operator):
    """Construct a QR code mesh"""
    bl_idname = "abc.make_aztec"
    bl_label = "Aztec Code"
    bl_options = {'REGISTER', 'UNDO'}

    data: bpy.props.StringProperty(
        name="Data",
        description="Data to store in the Aztec code. "
                    "More data generates a larger code",
        default="text")
    invert: bpy.props.BoolProperty(
        name="Invert",
        description="Create mesh in the dark areas instead of light. "
                    "The module in the very center should be dark, "
                    "but Aztec codes should still be readable inverted",
        default=False)
    border: bpy.props.IntProperty(
        name="Border",
        description="Border width to maintain quiet space. "
                    "Note: Aztec codes do not need quiet space, "
                    "however quiet space does not hurt"
                    "(disabled when inverted)",
        default=0, min=0, max=10)
    rescale: bpy.props.BoolProperty(
        name="Rescale",
        description="If true: Scale the QR code to specific size. "
                    "Otherwise, each module is one unit",
        default=True)
    # rescale_axis: bpy.props.EnumProperty(
    #     items=[('X', "X (default)", "Scale along X"),
    #            ('Y', "Y", "Scale along Y")],  # ('Z', "Z", "Scale along Z")]
    #     name="Resize axis",
    #     description="Choose axis to rescale to length",
    #     default='X')
    size: bpy.props.FloatProperty(
        name="Axis length",
        description="Specify the final dimensions of the QR code",
        default=1, min=0)
    join: bpy.props.BoolProperty(
        name="Join blocks",
        description="Join vertices of adjacent blocks. Same as merge vertices by distance or remove doubles",
        default=True)
    center: bpy.props.BoolProperty(
        name="Center on cursor",
        description="Centers the generated code on the 3D cursor.",
        default=False)

    '''
    security: bpy.props.IntProperty(
        name="Security",
        description="Sets the error correction level. "
                    "Generates a bigger code but can survive more damage. ",
        default=0, min=0, max=8)
    ratio: bpy.props.FloatProperty(
        name="Ratio",
        description="Specify the module height ratio. "
                    "PDF417 modules are tall and narrow. "
                    "They can still be read at different ratios, "
                    "but it's not reliable",
        default=3, min=0)
    '''

    def create_aztec_table(self):
        array = numpy.asarray(AztecCode(self.data).matrix)
        # produces an array of ' ' and '#'
        # converts it into bool
        array = array == '#'
        return array

    def execute(self, context):

        # aztec_table = self.create_aztec_table()

        try:
            aztec_table = self.create_aztec_table()
        except Exception as ex:
            print(str(ex))
            self.report({'ERROR'}, str(ex))
            return {'CANCELLED'}


        if not self.invert:
            aztec_table = build_borders(aztec_table, self.border, 1)

        aztec_obj = build_obj_from_table(
            context,
            aztec_table,
            1,
            self.invert,
            self.join,
            name="AztecCode")

        # optionally rescales the QR code object
        if self.rescale:
            resize_along_axis(aztec_obj, self.size, 'X')

        # optionally centers the object on the 3D cursor
        if self.center:
            center_on_cursor(aztec_obj)
        else:
            move_origin_3d_cursor(aztec_obj)

        return {'FINISHED'}
