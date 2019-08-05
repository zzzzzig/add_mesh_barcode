
import bpy
import bmesh
import numpy
# from math import radians
from bpy_extras import object_utils

"""
def diff_list(self, li1, li2):
    '''Compares two lists and returns the differences as a list.
    remove self when moving to shared file?'''
    return [i for i in li1 + li2 if i not in li1 or i not in li2]


def import_svg(svg_loc):
    '''Makes a Bunch of curves from the given svg file.
    Unintendedly, it puts them in a new collection named after the svg
    file. Merges them, renames them.
    returns the final object.
    It cannot count on the collection name to be identical, because it renames
    in case of doubles. Therefore, it compares a before and after list to
    find the new one. It works, but feels super wrong. Apparently, I
    shouldn't use operators for scripting. I tried using the function
    "load_svg" from io_curve_svg.import_svg. Same exact results. Super'''
    active_col = bpy.context.collection
    # print("active collection is :", active_col)
    # adds all existing collections to list old_col
    old_col = []
    for collection in bpy.data.collections:
        old_col.append(collection)
    # temp until i create a settings menu for temp barcode storage
    from pathlib import Path #pathlib is super useful for fixing slashes
    data_folder = Path("E:/zMedia/01.Creation/01.3D/01.Blender/01.Projects/000_Sketches/20190728_BarcodeDev/")
    svg_to_open = data_folder / "barcode.svg"
    # imports the SVG file as curves.
    # seems to make a new collection for many new curves.
    # bpy.ops.import_curve.svg(filepath=str(svg_to_open), filter_glob="*.svg")
    # use the function, not the operator
    from io_curve_svg.import_svg import load_svg
    # load_svg(context, filepath, do_colormanage)
    load_svg(bpy.context, str(svg_to_open), False)
    # adds all existing collections to list new_col
    new_col = []
    for collection in bpy.data.collections:
        new_col.append(collection)
    # compare collections before and after to find the new one
    # svg_col = self.diff_list(old_col, new_col)  # should i bother with a function for this?
    svg_col_list = [i for i in old_col + new_col if i not in old_col or i not in new_col]
    svg_col = svg_col_list[0]
    # deselects everything first so as to not merge with existing objects
    for obj in bpy.data.objects:
        obj.select_set(state=False)
    # selects the new curves
    for obj in svg_col.objects:
        obj.select_set(True)
    # makes the 0th one active. seems somewhat unpredictable
    # but doesnt really matter which one it is
    bpy.context.view_layer.objects.active = svg_col.objects[0]
    bpy.ops.object.join()
    svg_obj = svg_col.objects[0]
    # placeholder for something better. maybe just barcode specific name.
    # maybe something like: "pdf417 data goes he..." to help remember
    # which code is which.
    svg_obj.name = "barcode"
    # print("linking ", svg_obj.name, " to collection ", active_col)
    active_col.objects.link(svg_obj)
    # print("removing ", svg_obj.name, " from collection ", svg_col)
    svg_col.objects.unlink(svg_obj)
    # print("unlinking collection ", svg_col, " from scene")
    bpy.context.scene.collection.children.unlink(svg_col)  # unlinks the collection
    # print("removing collection ", svg_col)
    bpy.data.collections.remove(svg_col)  # removes the collection
    # remove junk svg material
    # active_mat_index = svg_obj.active_material_index
    bpy.ops.object.material_slot_remove()
    # optionally move to 3d cursor
    svg_obj.location = bpy.context.scene.cursor.location
    return svg_obj, active_col


def mesh_from_curve(curve_obj, active_col, merge_faces):
    # apparently since 2.8 this is the way to do it, not to_mesh()
    dg = bpy.context.evaluated_depsgraph_get()
    curve_obj_eval = curve_obj.evaluated_get(dg)
    curve_obj_data = bpy.data.meshes.new_from_object(curve_obj_eval)
    curve_name = curve_obj.name
    new_obj = bpy.data.objects.new(name="temp", object_data=curve_obj_data)
    # print("removing ", curve_obj.name, " from collection ", active_col)
    active_col.objects.unlink(curve_obj)
    # print("linking ", new_obj.name, " to collection ", active_col)
    active_col.objects.link(new_obj)
    new_obj.name = curve_name
    new_obj.matrix_world = curve_obj.matrix_world
    # limited dissolve to un- triangulate the faces
    mesh = new_obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.dissolve_limit(bm, angle_limit=radians(1), verts=bm.verts, edges=bm.edges)
    # merge doubles
    if merge_faces:
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
    bm.to_mesh(mesh)
    mesh.update()
    bm.clear()
    bm.free()

    return new_obj
"""

def resize_along_axis(obj, new_length, axis):
    # only works in object mode
    x_length, y_length, z_length = obj.dimensions
    if axis == 'X':
        # note, this works, but is not really intended by the devs
        obj.dimensions = [new_length, y_length, z_length]
        x_scale, y_scale, z_scale = obj.scale
        obj.scale = (x_scale, x_scale, z_scale)
    elif axis == 'Y':
        obj.dimensions = [x_length, new_length, z_length]
        x_scale, y_scale, z_scale = obj.scale
        obj.scale = (y_scale, y_scale, z_scale)
    elif axis == 'Z':
        # these barcodes are all suposed to be 2d.
        # If there's a z to rescale, something went wrong.
        print("potion seller, I whould like you to rescale on the Z")
        print("I cant do that traveler. You are too weak for my Z.")
    bpy.ops.object.transform_apply(scale=True)


def move_origin_3d_cursor(obj):
    # works on all selected objects. Make sure only the target is selected
    for object in bpy.data.objects:
        object.select_set(state=False)
    obj.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')


def center_on_cursor(obj):
    # Assumes the object is already one corner on the cursor
    # this is the case for all barcodes made by this addon
    x_length, y_length, z_length = obj.dimensions
    x_loc, y_loc, z_loc = obj.location
    obj.location.x = x_loc - (x_length / 2)
    obj.location.y = y_loc + (y_length / 2)
    move_origin_3d_cursor(obj)
    for object in bpy.data.objects:
        object.select_set(state=False)
    obj.select_set(True)


def draw_module(x, y, x_scale, y_scale, mesh):
    verts = [
        mesh.verts.new((x_scale * x,     y_scale * y,     0)),
        mesh.verts.new((x_scale * x,     y_scale * (y+1), 0)),
        mesh.verts.new((x_scale * (x+1), y_scale * (y+1), 0)),
        mesh.verts.new((x_scale * (x+1), y_scale * y,     0))
    ]
    # makes loose verts into faces
    mesh.faces.new(verts)


def draw_table(array, x_scale, y_scale, invert, mesh):
    not_invert = not invert
    for row_id in range(len(array)):
        for col_id in range(len(array[0])):
            visible = array[row_id][col_id]
            # print(visible, " is type ", type(visible))
            x = col_id
            y = row_id
            if visible ^ not_invert:
                draw_module(x, y, x_scale, y_scale, mesh)


def build_borders(array, borders, ratio):
    v_width = borders
    h_width = borders * round(ratio) if round(ratio) > 1 else borders

    # add border padding to array
    array = numpy.pad(array,
                      ((v_width, v_width), (h_width, h_width)),
                      'constant',
                      constant_values=0)
    return array


def build_obj_from_table(context,
                         table,
                         ratio,
                         invert,
                         join=True,
                         name='Barcode'):
    # only works in object mode
    x_scale = 1
    y_scale = -1 * ratio

    # creates a new bmesh to play with
    mesh = bmesh.new()

    draw_table(table, x_scale, y_scale, invert, mesh)
    if join:
        bmesh.ops.remove_doubles(mesh, verts=mesh.verts, dist=0.0001)
    # generates a new blank mesh datablock
    mesh_block = bpy.data.meshes.new(name)
    # adds bmesh data to datablock
    mesh.to_mesh(mesh_block)
    # deletes the now used bmesh
    mesh.free()
    # makes a new object for the mesh datablock to live in
    mesh_obj = object_utils.object_data_add(context, mesh_block)
    mesh_obj.name = name
    return mesh_obj
