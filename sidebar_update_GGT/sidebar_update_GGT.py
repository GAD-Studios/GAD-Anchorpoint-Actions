import os
import anchorpoint as ap


def on_timeout(ctx: ap.Context):
    # This code will be automatically executed once every minute
    try:
        project_path = ctx.project_path

        # Check if GAD-git-tools is the project path directory
        if os.path.exists(os.path.join(project_path, "GAD-git-tools")):
            # Run the auto update script with --need-update flag using full path
            script_path = os.path.join(project_path, "GAD-git-tools/scripts/auto_update.py")
            result = os.popen(f"python3 {script_path} --need-update").read().strip()
            
            # If updates are needed (result is "true"), show notification
            if result == "true":
                ui = ap.UI()
                ui.show_info("GAD-git-tools updates available")
                ctx.icon_color = "red"
    except Exception as e:
        print(f"Error in on_timeout: {str(e)}")
        ui = ap.UI()
        ui.show_error(f"Error checking for GAD-git-tools updates: {str(e)}")

# When the sidebar button is clicked, do an explicit update of GAD-git-tools
if __name__ == "__main__":
    try:
        ctx = ap.get_context()
        project_path = ctx.project_path

        # Check if GAD-git-tools is the project path directory
        if os.path.exists(os.path.join(project_path, "GAD-git-tools")):
            # Run the auto update script using full path
            script_path = os.path.join(project_path, "GAD-git-tools/scripts/auto_update.py")
            result = os.system(f"python3 {script_path}")
            
            if result == 0:
                ui = ap.UI()
                ui.show_info("GAD-git-tools updated successfully")
            else:
                raise Exception(f"Update script returned error code: {result}")
        else:
            raise Exception("GAD-git-tools directory not found")
            
    except Exception as e:
        print(f"Error in main: {str(e)}")
        ui = ap.UI()
        ui.show_error(f"Error updating GAD-git-tools: {str(e)}")
