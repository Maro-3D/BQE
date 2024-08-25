import bpy

# Define the operator
class QUICKEXPORT_OT_export(bpy.types.Operator):
    bl_idname = "quickexport.export"
    bl_label = "Quick Export"
    bl_description = "Exports the collection containing the active object."

    # Function to dynamically get collections with exporters
    def get_collection_items(self, context):
        active_obj = context.active_object
        if active_obj:
            # Only include collections with exporters
            collections = [col for col in bpy.data.collections if active_obj.name in col.objects and hasattr(col, 'exporters') and len(col.exporters) > 0]
            return [(col.name, col.name, "") for col in collections]
        return []

    # EnumProperty for selecting a collection
    collection_items: bpy.props.EnumProperty(
        name="Collection",
        description="Select a collection to export",
        items=get_collection_items
    )
    
    # Poll function to enable/disable the button
    @classmethod
    def poll(cls, context):
        active_obj = context.active_object
        if not active_obj:
            cls.poll_message_set("No active object selected")
            return False
        # Check if any collection with exporters exists
        collections_with_exporters = any(
            col for col in bpy.data.collections if active_obj.name in col.objects and hasattr(col, 'exporters') and len(col.exporters) > 0
        )
        if not collections_with_exporters:
            cls.poll_message_set("No collections with exporters found for the active object")
        return collections_with_exporters
    
    def execute(self, context):
        # Check if there is an active object
        active_obj = context.active_object
        if not active_obj:
            self.report({'WARNING'}, "No active object selected")
            return {'CANCELLED'}
        
        # Get the collection selected by the user
        selected_collection_name = self.collection_items
        selected_collection = bpy.data.collections.get(selected_collection_name)
        
        # If a valid collection is selected, proceed with exporting
        if selected_collection:
            self.export_collection(context, selected_collection)
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "No valid collection selected")
            return {'CANCELLED'}

    # Display popup with a dropdown menu to choose the collection if there are multiple
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "collection_items", text="Collection")

    # Function to handle the actual export logic
    def export_collection(self, context, collection):
        # Store the original active collection
        original_collection = context.view_layer.active_layer_collection
        
        # Find the layer collection that matches the collection to be exported
        for layer_col in context.view_layer.layer_collection.children:
            if layer_col.collection == collection:
                # Set the active layer collection to the desired collection
                context.view_layer.active_layer_collection = layer_col
                break
       
        # Call the Export all function
        bpy.ops.collection.export_all()
        
        # Print to console which collection is being exported
        self.report({'INFO'}, f"Successfully exported collection: '{layer_col.name}'.")
        
        # Restore the original active collection
        context.view_layer.active_layer_collection = original_collection

        return {'FINISHED'}
    
    def invoke(self, context, event):
        active_obj = context.active_object
        # Filter collections to include only those with exporters
        collections = [col for col in bpy.data.collections if active_obj and active_obj.name in col.objects and hasattr(col, 'exporters') and len(col.exporters) > 0]
        
        # If multiple collections, show the popup dialog
        if len(collections) > 1:
            return context.window_manager.invoke_props_dialog(self)
        elif len(collections) == 1:
            # If only one collection, export directly
            self.export_collection(context, collections[0])
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "Active object is not in any collection with exporters")
            return {'CANCELLED'}
    
# Function to draw the button in the top bar
def draw_quick_export_button(self, context):
    layout = self.layout
    layout.operator("quickexport.export", text="",icon="EXPORT")

# Register the operator and append the button to the top bar
def register():
    bpy.utils.register_class(QUICKEXPORT_OT_export)
    bpy.types.TOPBAR_MT_editor_menus.append(draw_quick_export_button)

# Unregister the operator and remove the button from the top bar
def unregister():
    bpy.utils.unregister_class(QUICKEXPORT_OT_export)
    bpy.types.TOPBAR_MT_editor_menus.remove(draw_quick_export_button)

if __name__ == "__main__":
    register()
