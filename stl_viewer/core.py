"""View STL files if provided as an attachment to a part"""

from part.models import Part
from common.models import InvenTreeSetting
from django.db.models import Q

from django.core.exceptions import ValidationError

from plugin import InvenTreePlugin
from plugin.mixins import SettingsMixin, UserInterfaceMixin

from . import PLUGIN_VERSION


def is_hex_color(color: str):
    """Determines whether the input is a valid hex color code."""

    error_text = "Must be a hex code of form '#44db44'"

    if len(color) != 7 or not color.startswith("#"):
        raise ValidationError(error_text)

    for char in color[1:]:
        char_ord = ord(char.lower())
        if not (48 <= char_ord <= 57 or 97 <= char_ord <= 102):
            raise ValidationError(error_text)

    return True


class STLViewer(SettingsMixin, UserInterfaceMixin, InvenTreePlugin):
    """STLViewer - custom InvenTree plugin."""

    # Plugin metadata
    TITLE = "STL Viewer"
    NAME = "STLViewer"
    SLUG = "stl-viewer"
    DESCRIPTION = "View STL files if provided as an attachment to a part"
    VERSION = PLUGIN_VERSION

    # Additional project information
    AUTHOR = "Alec Delaney"
    WEBSITE = "https://github.com/tekktrik/inventree-stl-viewer-plugin"
    LICENSE = "MIT"

    # Optionally specify supported InvenTree versions
    # MIN_VERSION = '0.18.0'
    # MAX_VERSION = '2.0.0'

    # Plugin settings (from SettingsMixin)
    # Ref: https://docs.inventree.org/en/latest/plugins/mixins/settings/
    USER_SETTINGS = {
        # Define your plugin settings here...
        "MODEL_COLOR": {
            "name": "Model Color",
            "description": "Color for the model",
            "validator": [
                str,
                is_hex_color,
            ],
            "default": "#44db44",
        }
    }

    # User interface elements (from UserInterfaceMixin)
    # Ref: https://docs.inventree.org/en/latest/plugins/mixins/ui/

    # Custom UI panels
    def get_ui_panels(self, request, context: dict, **kwargs):
        """Return a list of custom panels to be rendered in the InvenTree user interface."""

        # Only display this panel for the 'part' target
        if context.get("target_model") != "part":
            return []

        base_url = InvenTreeSetting.get_setting("INVENTREE_BASE_URL")

        primary_key = context.get("target_id")
        part = Part.objects.get(pk=primary_key)

        attachments = part.attachments.filter(Q(attachment__endswith=".stl"))

        if not attachments:
            return []

        attachement_urls = [
            f"{base_url}/media/{attachment.attachment.name}"
            for attachment in attachments
        ]

        panels = []

        panels.append({
            "key": "stl-viewer-panel",
            "title": "STL Viewer",
            "description": "Custom panel description",
            "icon": "ti:file-3d:outline",
            "source": self.plugin_static_file("Panel.js:renderSTLViewerPanel"),
            "context": {
                # Provide additional context data to the panel
                "attachments": attachement_urls,
                "model_color": self.get_user_setting("MODEL_COLOR", request.user),
            },
        })

        return panels
