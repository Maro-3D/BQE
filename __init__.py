import bpy

bl_info = {
    "name": "Quick Export",
    "author": "Marek Hanzelka",
    "version": (1, 1, 0),
    "blender": (4, 2, 0),
    "location": "Outliner",
    "description": "Exports the collection containing the active object.",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": "Import-Export"
}

class QUICKEXPORT_OT_export(bpy.types.Operator):
    """Operator to export the first collection containing the active object that has exporters."""
    bl_idname = "quickexport.export"
    bl_label = "Quick Export"
    bl_description = "Exports the collection containing the active object."

    def find_exportable_collection(self, obj):
        """Find the first collection that has exporters, starting from the collection containing the active object."""
        for collection in bpy.data.collections:
            if obj.name in collection.objects:
                # Traverse up the hierarchy until we find a collection with an exporter
                while collection:
                    if hasattr(collection, 'exporters') and collection.exporters:
                        # Collect exporter names
                        exporter_names = [exp.name for exp in collection.exporters]
                        return collection, exporter_names
                    collection = self.get_parent_collection(collection)
        return None, []

    def get_parent_collection(self, collection):
        """Find the parent collection from the view layer."""
        for layer_collection in bpy.context.view_layer.layer_collection.children:
            parent = self.search_in_layer_collection(layer_collection, collection)
            if parent:
                return parent
        return None

    def search_in_layer_collection(self, layer_collection, target_collection):
        """Recursively search for the parent collection in layer collections."""
        # Compare using collection names
        if target_collection.name in [child.name for child in layer_collection.collection.children]:
            return layer_collection.collection
        for child_layer in layer_collection.children:
            parent = self.search_in_layer_collection(child_layer, target_collection)
            if parent:
                return parent
        return None

    def export_collection(self, context, collection, exporter_names):
        """Perform the export."""
        original_collection = context.view_layer.active_layer_collection
        layer_col = self.find_layer_collection(context.view_layer.layer_collection, collection)

        if layer_col:
            context.view_layer.active_layer_collection = layer_col
            if hasattr(bpy.ops.collection, 'export_all'):
                bpy.ops.collection.export_all()
                # Include the exporter names in the success message
                exporter_names_str = ", ".join(exporter_names)
                self.report({'INFO'}, f"Successfully exported collection: '{layer_col.name}' using exporters: {exporter_names_str}")
            else:
                self.report({'ERROR'}, "No valid export operator found.")
            context.view_layer.active_layer_collection = original_collection
        else:
            self.report({'WARNING'}, "Could not find the layer collection for exporting.")

    def find_layer_collection(self, layer_collection, collection):
        """Search for the layer collection corresponding to a specific collection."""
        if layer_collection.collection == collection:
            return layer_collection
        for child in layer_collection.children:
            result = self.find_layer_collection(child, collection)
            if result:
                return result
        return None

    def execute(self, context):
        """Execute the export by finding and exporting the correct collection."""
        active_obj = context.active_object
        if not active_obj:
            self.report({'WARNING'}, "No active object selected")
            return {'CANCELLED'}
        
        # Find the exportable collection and get the exporter names
        exportable_collection, exporter_names = self.find_exportable_collection(active_obj)

        if exportable_collection:
            self.export_collection(context, exportable_collection, exporter_names)
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "No collection with exporters found for the active object.")
            return {'CANCELLED'}

# Function to draw the button in the top bar
def draw_quick_export_button(self, context):
    layout = self.layout
    layout.operator("quickexport.export", text="",icon="EXPORT", emboss = False)


# Register the operator and append the button to the Outliner
def register():
    bpy.utils.register_class(QUICKEXPORT_OT_export)
    bpy.types.TOPBAR_MT_editor_menus.append(draw_quick_export_button)

# Unregister the operator and remove the button from the Outliner
def unregister():
    bpy.utils.unregister_class(QUICKEXPORT_OT_export)
    bpy.types.TOPBAR_MT_editor_menus.remove(draw_quick_export_button)

if __name__ == "__main__":
    register()
