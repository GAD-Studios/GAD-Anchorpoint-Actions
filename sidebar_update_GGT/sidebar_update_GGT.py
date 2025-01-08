import os
import anchorpoint as ap


def on_timeout(ctx: ap.Context):
    # This code will be automatically executed once every minute
    project_path = ctx.project_path

    # Check if GAD-git-tools is the project path directory
    if os.path.exists(os.path.join(project_path, "GAD-git-tools")):
        # Run the auto update script with --need-update flag
        result = os.popen("python3 GAD-git-tools/scripts/auto_update.py --need-update").read().strip()
        
        # If updates are needed (result is "true"), show notification
        if result == "true":
            ui = ap.UI()
            ui.show_info("GAD-git-tools updates available")
            ctx.icon_color = "red"

# When the sidebar button is clicked, do an explicit update of GAD-git-tools
if __name__ == "__main__":
	ctx = ap.get_context()

	project_path = ctx.project_path

	# Check if GAD-git-tools is the project path directory
	if os.path.exists(os.path.join(project_path, "GAD-git-tools")):
		# Run the auto update script
		os.system("python3 GAD-git-tools/scripts/auto_update.py")
	
		ui = ap.UI()
		ui.show_info("GAD-git-tools updated")
