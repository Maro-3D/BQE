## Quick Export Collection Addon

### Overview

**Quick Export** is a Blender addon designed to streamline the process of exporting collections that contain the active object. The addon identifies collections that have an active exporter setup and allows users to quickly export the collection with just a few clicks.

### Features

- Automatically identifies collections containing the active object.
- Only displays collections with active exporters.
- Provides a quick export button directly in the top bar for easy access.
- Includes tooltips and messages to guide users through the export process.

### Installation

1. Download the addon `.py` file or copy the script code.
2. Open Blender.
3. Go to `Edit` > `Preferences`.
4. In the Preferences window, navigate to the `Add-ons` section.
5. Click the `Install` button at the top.
6. Select the `.py` file you downloaded or copied.
7. Enable the addon by checking the box next to **Quick Export Collection**.

### Usage

1. Ensure an object is selected in your scene.
2. The **Quick Export** button will appear in the top bar.
3. Click the **Quick Export** button.
4. If the object is part of multiple collections with exporters, select the desired collection from the dropdown menu.
5. The collection will be exported, and a message will appear confirming the export.

### Requirements

- Blender 4.2.0 or newer!!!

### Troubleshooting

- **No active object selected**: Ensure you have selected an object in the 3D viewport before using the addon.
- **No collections with exporters found**: Make sure the active object is part of a collection that has an active exporter setup.



