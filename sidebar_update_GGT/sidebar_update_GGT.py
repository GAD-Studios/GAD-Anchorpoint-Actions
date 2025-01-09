import os
import anchorpoint as ap
import subprocess
import sys


def on_timeout(ctx: ap.Context):
    # This code will be automatically executed once every minute
    # In the future we could just check for updates here, but there's no way to change
    # icon colors in the sidebar at runtime, so it would not be very helpful.
    update_gad_git_tools(ctx)

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
        
def update_gad_git_tools(ctx: ap.Context):
    if not check_gad_git_tools(ctx):
        return
    else:
        try:
            project_path = ctx.project_path

            # Check if GAD-git-tools is the project path directory
            if os.path.exists(os.path.join(project_path, "GAD-git-tools")):
                # Run the auto update script using full path and capture output
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
                    ui = ap.UI()
                    ui.show_info("GAD-git-tools updated successfully")
            else:
                raise Exception("GAD-git-tools directory not found")
                
        except Exception as e:
            print(f"Error in main: {str(e)}")
            ui = ap.UI()
            ui.show_error(f"Error updating GAD-git-tools: {str(e)}")

# When the sidebar button is clicked, do an explicit update of GAD-git-tools
if __name__ == "__main__":
	ctx = ap.get_context()
	update_gad_git_tools(ctx)