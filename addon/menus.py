
import bpy

from bpy.types import Menu


class ABC_MT_barcode_2d_add(Menu):
    ''' Define the "Add Mesh > Barcode >" menu '''
    bl_idname = "ABC_MT_barcode_2d_add"
    bl_label = "2D"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.separator()
        self.layout.operator("abc.make_qrcode",
                            text = "QR Code",
                            icon = 'PLUGIN')

        self.layout.operator( "abc.make_pdf417",
                            text = "PDF417",
                            icon = 'PLUGIN')

        self.layout.operator( "abc.make_aztec",
                            text = "Aztec",
                            icon = 'PLUGIN')


"""
class ABC_MT_barcode_1d_add(Menu):
    ''' Define the "Add Mesh > Barcode >" menu '''
    bl_idname = "ABC_MT_barcode_1d_add"
    bl_label  = "1D"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.separator()
        self.layout.operator("abc.make_barcode",
                            text = "Barcode",
                            icon = 'PLUGIN')
"""

"""
class ABC_MT_barcode_add(Menu):
    ''' Define the "Add Mesh > Barcode >" menu '''
    bl_idname = "ABC_MT_barcode_add"
    bl_label = "Barcode"

    def draw(self, context):
        layout                  = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.separator()
        layout.menu("ABC_MT_barcode_1d_add",
                    text = "1D",
                    icon = 'PLUGIN')

        layout.menu("ABC_MT_barcode_2d_add",
                    text = "2D",
                    icon = 'PLUGIN')
"""

class ABC_MT_barcode_add(Menu):
    ''' Define the "Add Mesh > Barcode >" menu '''
    bl_idname = "ABC_MT_barcode_add"
    bl_label = "Barcode"

    def draw(self, context):
        layout                  = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.separator()
        self.layout.operator("abc.make_qrcode",
                            text = "QR Code",
                            icon = 'PLUGIN')

        self.layout.operator( "abc.make_pdf417",
                            text = "PDF417",
                            icon = 'PLUGIN')

        self.layout.operator( "abc.make_aztec",
                            text = "Aztec",
                            icon = 'PLUGIN')

def menu_func(self, context):
    # adds entry for "Barcode" in whatever menu it is called in
    layout = self.layout
    layout.operator_context = 'INVOKE_REGION_WIN'

    layout.separator()
    layout.menu("ABC_MT_barcode_add",
                text = "Barcode",
                icon = 'PLUGIN')