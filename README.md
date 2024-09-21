### Overview

**Quick Export** is a Blender addon designed to streamline the exporting process by enabling users to export the collection containing the active object with a single click. This tool is particularly useful for users who frequently export specific collections and need a fast, efficient way to do so.

### How to Use

1. **Select an Active Object:** Choose an object you wish to export.

2. **Click the Export Button:** In the Outliner, click the "Quick Export" button to export the collection containing the selected object. For faster exporting, it is recommended to add the Quick Export button to the Quick Favorites by right-clicking on the export button and selecting "Add to Quick Favorites." Then, you can quickly access it by pressing `Q` and choosing "Quick Export."

3. **Automatic Export:** The addon will find the relevant collection and export it using the associated exporters.

### How it Works

The addon searches for the first collection that has exporters, starting from the collection containing the active object. If a valid collection is found, it stops and uses the appropriate exporter to perform the export of the found collection. If multiple exporters are available, they are all utilized.

### Installation

1. Download the addon `.py` file or copy the script code.
2. Open Blender.
3. Go to `Edit` > `Preferences`.
4. In the Preferences window, navigate to the `Add-ons` section.
5. Click the `Install` button at the top.
6. Select the `.py` file you downloaded or copied.
7. Enable the addon by checking the box next to **Quick Export Collection**.

### Requirements

- Blender 4.2.0 or newer!!!
