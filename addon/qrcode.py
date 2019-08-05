
import bpy
# import bmesh
# from bpy_extras import object_utils
from .. generators import segno

from . shared import resize_along_axis
from . shared import move_origin_3d_cursor, center_on_cursor
from . shared import build_borders, build_obj_from_table


# naming is AAA_BB_CC
# AAA = normal use space (e.g. "VIEW3D"), or a unique string per addon. all caps
# BB  = 
class ABC_OT_mesh_qrcode(bpy.types.Operator):
    """Construct a QR code mesh"""
    bl_idname = "abc.make_qrcode"
    bl_label = "QR Code"
    bl_options = {'REGISTER', 'UNDO'}

    data: bpy.props.StringProperty(
        name="Data",
        description="Data to store in the QR code. "
                    "Can be Text, numbers, or many symbols. "
                    "More data produces larger codes.",
        default="text")
    qr_micro: bpy.props.EnumProperty(
        items=[ ('auto',  "Auto",         "Micro or normal based on data size. MicroQR readers are very rare"),
                ('qr',    "QR (Default)", "Forces standard QR Code generation"),
                ('micro', "Micro",        "Micro QR code - readers are very rare")],
        name   ="QR code type",
        description="What type of QR code to Generate. "
                    "Micro QR codes have a higher information density, but much smaller max size, an consequently, storage capacity. "
                    "Both Micro QR codes and readers are very rare."
                    "(Default: QR)",
        default='qr')
    ec_mode: bpy.props.EnumProperty(
        items=[ ('A',    "Auto (default)", "Automatically picks highest value without raising version"),
                ('L',    "L",              "Correct up to 7% damage"),
                ('M',    "M",              "Correct up to 15% damage"),
                ('Q',    "Q",              "Correct up to 25% damage"),
                ('H',    "H",              "Correct up to 30% damage")],
        name="Error correction",
        description="Allows QR data to be read after damage."
                    "Auto picks the highest value that does not require a higher version QR Code. "
                    "Note, no level of error correction can make up for damaged Position or Allignment squares. "
                    "Aditionally, the timing indicators between the large allignment squares cannot be damaged either."
                    "(Default:Auto)",
        default='A')
    qr_version: bpy.props.IntProperty(
        name="Version",
        description="QR Version. Allows forcing larger codes than the data requires. "
                    "0 Is Auto. "
                    "Version describes size of the QR code. "
                    "Auto generates the smallest code that can hold the data with the specified Error Correction. "
                    "Ignored for micro codes. (Default:0)",
        default=0, min=0, max=40)
    '''
    qr_mode: bpy.props.EnumProperty(
                    items=[ ('A',            "Auto (Default)", "Automatically chooses encoder mode"),
                            ('numeric',      "Numeric",        "Allows storing numbers"),
                            ('alphanumeric', "Alphanumeric",   "Allows storing letters and numbers"),
                            ('byte',         "Byte",           "Allows storing byte data. 1 or 0"),
                            ('kanji',        "Kanji",          "Correct up to 25% damage")],
                    name   ="Data mode",
                    description="Force generation of a specific type of code. Default is Auto."
                                "Note, I couldnt get kanji to work."
                                "It should work if blender can handle kanji text."
                                "Alphanumeric seems not to work for text. Overall, stick to auto for text or numeral for numbers.",
                    default='A')
    '''
    invert: bpy.props.BoolProperty(
        name="Invert",
        description="Create mesh in the dark areas instead of light. "
                    "Dots in center of corner squares should be dark. "
                    "Some readers can handle white on black codes, but they "
                    "are rare",
        default=False)
    border: bpy.props.IntProperty(
        name="Border",
        description="Border width to maintain quiet space around code. "
                    "QR codes need a blank space around them in order to be read. "
                    "(disabled when inverted)",
        default=2, min=0, max=10)
    join: bpy.props.BoolProperty(
        name="Join blocks",
        description="Join vertices of adjacent blocks. Same as merge vertices by distance or remove doubles",
        default=True)
    rescale: bpy.props.BoolProperty(
        name="Rescale",
        description="If true: Scale the QR code to specific size. "
                    "Otherwise, each module is one unit",
        default=True)
    size: bpy.props.FloatProperty(
        name="Scale",
        description="Specify the final dimensions of the QR code",
        default=1, min=0)
    center: bpy.props.BoolProperty(
        name="Center on cursor",
        description="Centers the generated code on the 3D cursor",
        default=False)
    '''
    debug: bpy.props.BoolProperty(
        name="Debug",
        description="Show intended QR in default PNG viewer",
        default=False)
    '''

    def create_qrcode_table(self):
        # segno.make_qr(content, error=, version=,
        #               mode=,   mask=,  encoding=,
        #               eci=,    boost_error=)
        # Opening logic
        make_micro_dict = {'auto' : None, 'qr' : False, 'micro' : True} # makes a dictionary to fix the true/false strings while making A = None
        make_micro = make_micro_dict[self.qr_micro]

        qr = segno.make(
            self.data,
            error       = None if self.ec_mode    == 'A' else self.ec_mode,
            boost_error = True if self.ec_mode    == 'A' else False,
            version     = None if self.qr_version == 0 or make_micro else self.qr_version,
            # mode        = None if self.qr_mode    == 'A' else self.qr_mode,
            mode        = None,
            micro       = make_micro # None if self.qr_micro   == 'A' else bool(self.qr_micro)  # not working. working when directly stated
            )
        '''
        if self.debug:
            qr.show()
        '''
        return qr.matrix

    def execute(self, context):

        # qr_table = self.create_qrcode_table()

        try:
            qr_table = self.create_qrcode_table()
        except ValueError as ex:
            error_report = "\n".join(ex.args)
            print(str(ex))
            self.report({'ERROR'}, str(ex))
            return {'CANCELLED'}

        if not self.invert:
            qr_table = build_borders(qr_table, self.border, 1)

        qr_obj = build_obj_from_table(
            context,
            qr_table,
            1,
            self.invert,
            self.join,
            name="QRCode")

        # optionally rescales the QR code object
        if self.rescale:
            resize_along_axis(qr_obj, self.size, 'X')

        # optionally centers the object on the 3D cursor
        if self.center:
            center_on_cursor(qr_obj)
        else:
            move_origin_3d_cursor(qr_obj)

        return {'FINISHED'}


