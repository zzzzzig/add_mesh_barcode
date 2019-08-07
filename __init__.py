# Copyright (c) 2014 Jacob Welsh <jwelsh+blender@welshcomputing.com>
#
# MIT/X11 license:
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

'''
Copyright (C) 2019 zzzzzig
zzzzzig on blenderartists.org

Created by Jacob Welsh and zzzzzig

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

'''
note 2019-07-31: I (zzzzzig) have modified this plugin almost beyond
recognition. I do not know if the original license still applies, should be listed
here, or should be changed. I'll leave it up and add my own too.
'''

'''
The libraries used are:
Segno - https://github.com/heuer/segno - BSD 3-Clause "New" or "Revised" License
pdf417-py, also called pdf417gen - https://github.com/ihabunek/pdf417-py - MIT License
aztec_code_generator - https://github.com/delimitry/aztec_code_generator - MIT License

'''



# Info that shows up in the addon list
bl_info = {
    "name": "Local Barcodes",
    "description": "Add a Barcode mesh. Generates codes locally using various"
                   " libraries, not a web service. Heavily modified version "
                   "of local QRCode by Jacob Welsh.",
    "author": "Jacob Welsh, zzzzzig",
    "version": (0, 0, 2),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > Barcode",
    "wiki_url": "None",
    "category": "Add Mesh",
    "warning": "this addon is still in development"
}

#================================================================
# BUNDLE HEADER

if "bpy" in locals():
    print("Barcode: reloading modules")
    import importlib
    importlib.reload(shared)
    importlib.reload(qrcode)
    importlib.reload(pdf417)
    importlib.reload(aztec)
    # importlib.reload(linear)
    importlib.reload(menus)
else:
    print("Barcode: NOT reloading modules")
    from . addon import shared
    from . addon import qrcode
    from . addon import pdf417
    from . addon import aztec
    # from . addon import linear
    from . addon import menus
import bpy

# END BUNDLE HEADER
# ================================================================


classes = [
    qrcode.ABC_OT_mesh_qrcode,
    pdf417.ABC_OT_mesh_pdf417,
    aztec.ABC_OT_mesh_aztec,
    # linear.ABC_OT_mesh_barcode,
    menus.ABC_MT_barcode_add,
    # menus.ABC_MT_barcode_2d_add,
    # menus.ABC_MT_barcode_1d_add
]


def register():

    from bpy.utils import register_class
    for cls in classes:
       register_class(cls)

    # adds the Barcode submenu to the add mesh menu
    bpy.types.VIEW3D_MT_mesh_add.append(menus.menu_func)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    # removes the Barcode submenu from the add mesh menu
    bpy.types.VIEW3D_MT_mesh_add.remove(menus.menu_func)

# I have no idea what this does, and am too lazy to look it up
# some addons have it and some don't
if __name__ == "__main__":
    register()
