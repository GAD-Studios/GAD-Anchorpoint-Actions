import os
import anchorpoint as ap
import subprocess
import sys
from datetime import datetime


def on_timeout(ctx: ap.Context):
    # Only run once per hour by checking current hour
    if datetime.now().minute == 0:
        if check_gad_git_tools(ctx):
            update_gad_git_tools(ctx, show_success_toast=True)

def check_gad_git_tools(ctx: ap.Context):
    try:
        project_path = ctx.project_path

        # Check if GAD-git-tools is the project path directory
        if os.path.exists(os.path.join(project_path, "GAD-git-tools")):
            
            script_path = os.path.join(project_path, "GAD-git-tools/scripts/auto-update.py")
            
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            result = subprocess.run(
                [sys.executable, script_path, "--need-update", "--no-window"],
                capture_output=True,
                text=True,
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW,
                cwd=project_path
            )
            
            return "true" in result.stdout.strip().lower()
                
    except Exception as e:
        print(f"Error in on_timeout: {str(e)}")
        ui = ap.UI()
        ui.show_error(f"Error checking for GAD-git-tools updates: {str(e)}")
        
def update_gad_git_tools(ctx: ap.Context, show_success_toast=False):
    try:
        project_path = ctx.project_path

        # Check if GAD-git-tools is the project path directory
        if os.path.exists(os.path.join(project_path, "GAD-git-tools")):
            script_path = os.path.join(project_path, "GAD-git-tools/scripts/auto-update.py")
            
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            result = subprocess.run(
                [sys.executable, script_path, "--no-window"],
                capture_output=True,
                text=True,
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW,
                cwd=project_path
            )
            
            if result.returncode != 0:
                raise Exception(f"Update failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
            else:
                if show_success_toast:
                    ui = ap.UI()
                    ui.show_info("GAD-git-tools updated successfully")
                return True
        else:
            raise Exception("GAD-git-tools directory not found")
                
    except Exception as e:
        print(f"Error in main: {str(e)}")
        ui = ap.UI()
        ui.show_error(f"Error updating GAD-git-tools: {str(e)}")
        return False

# When the sidebar button is clicked, always attempt update and show result
if __name__ == "__main__":
    ctx = ap.get_context()
    update_gad_git_tools(ctx, show_success_toast=True)