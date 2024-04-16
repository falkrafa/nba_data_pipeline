import subprocess
import os 

def install_requirements():
    script_directory = os.path.dirname(os.path.realpath(__file__))
    requirements_file = os.path.join(script_directory, "requirements.txt")
    try:
        subprocess.check_call(["pip", "install", "-r", requirements_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("\033[1;32mRequirements installed successfully.\033[0m")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\033[1;31mError: Failed to install requirements - {e}\033[0m")
        return False

def run_docker_compose():
    try:
        subprocess.check_call(["docker-compose", "up", "-d", "--build"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("\033[1;32mDocker Compose command executed successfully.\033[0m")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\033[1;31mError: Failed to execute Docker Compose command - {e}\033[0m")
        return False
    
def run_script(script_path):
    try:
        subprocess.check_call(["python", script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return None
    except subprocess.CalledProcessError as e:
        return e 
    
def run_jobs():
    script_directory = "Jobs"
    scripts_to_run = [f for f in os.listdir(script_directory) if f.endswith('.py')]

    for script_name in scripts_to_run:
        script_path = os.path.join(script_directory, script_name)
        
        error = run_script(script_path)
        if error:
            print(f"\033[1;31mError: Failed to execute script {script_name} - {error}\033[0m")
            return False
        else:
            print(f"\033[1;32mScript {script_name} executed successfully.\033[0m")
    
    return True
        
if __name__ == "__main__":
    #os.system("cls")
    if install_requirements() and run_docker_compose() and run_jobs():
        print(f"\033[1;32mAll commands executed successfully.\033[0m")
    else:
        print(f"\n\033[1;31mA command failed. Aborting...\033[0m")