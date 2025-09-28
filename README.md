# STLViewer

View STL files if provided as an attachment to a part

## Installation

### InvenTree Plugin Manager

Admins for the InvenTree instance can use the Admin panel to directly add the plugin, by using the package name `inventree-stl-viewer`.

### Command Line 

To install manually via the command line, run the following command:

```bash
pip install inventree-stl-viewer
```

Add  `inventree-stl-viewer` to your InvenTree server's `plugins.txt`.

## Configuration

Users can set their preferred STL model color in their user settings.

## Usage

The STLViewer panel will automatically appear when looking at parts that have STL files as attachments!  There will be a tab for each STL file.
