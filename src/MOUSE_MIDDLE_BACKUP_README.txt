MOUSE MIDDLE BUTTON CONFIGURATION BACKUPS
=========================================

These backup files preserve your working WhisperWriter configuration with middle mouse button activation.

FILES:
------
- config_backup_mouse_middle.yaml     = Your personal settings with MOUSE_MIDDLE activation
- config_schema_backup_mouse_middle.yaml = Schema file with MOUSE_MIDDLE as default

HOW TO RESTORE:
---------------
If future updates overwrite your config and break the middle mouse button:

1. Restore your personal settings:
   copy config_backup_mouse_middle.yaml config.yaml

2. Restore the schema defaults (if needed):
   copy config_schema_backup_mouse_middle.yaml config_schema.yaml

3. Restart WhisperWriter

WHAT'S PRESERVED:
-----------------
✓ activation_key: MOUSE_MIDDLE (middle mouse button activation)
✓ recording_mode: press_to_toggle (your preferred mode)
✓ model: medium.en (your model choice) 
✓ compute_type: float32 (your performance setting)
✓ device: cuda (your GPU setting)
✓ All your other customized preferences

NOTES:
------
- Keep these backup files safe
- If you make new changes you like, update the backups
- These files ensure you can always restore the middle mouse button functionality 