import os
import anchorpoint as ap
import subprocess
import sys


def on_timeout(ctx: ap.Context):
    # This code will be automatically executed once every minute
    try:
        project_path = ctx.project_path

        # Check if GAD-git-tools is the project path directory
        if os.path.exists(os.path.join(project_path, "GAD-git-tools")):
            # Run the auto update script with --need-update flag using full path
            script_path = os.path.join(project_path, "GAD-git-tools/scripts/auto_update.py")
            result = subprocess.run(
                [sys.executable, script_path, "--need-update"],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # If updates are needed (output is "true"), show notification
            if result.stdout.strip() == "true":
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
            # Run the auto update script using full path and capture output
            script_path = os.path.join(project_path, "GAD-git-tools/scripts/auto_update.py")
            
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                raise Exception(f"Update failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
            else:
                ui = ap.UI()
                ui.show_info("GAD-git-tools updated successfully")
        else:
            raise Exception("GAD-git-tools directory not found")
            
    except Exception as e:
        print(f"Error in main: {str(e)}")
        ui = ap.UI()
        ui.show_error(f"Error updating GAD-git-tools: {str(e)}")
