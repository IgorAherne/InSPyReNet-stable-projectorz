import os
import sys
import subprocess

def main():
    """
    Uses InSPyReNet's run/Inference.py to remove backgrounds for images
    in ./code/input/ and produce RGBA outputs in ./code/output/.
    """
    script_dir = os.path.dirname(__file__)
    input_dir = os.path.join(script_dir, 'input')
    output_dir = os.path.join(script_dir, 'output')

    # If your InSPyReNet repo is in a sibling folder called "InSPyReNet-stable-projectorz"
    # adjust this path accordingly:
    inspyre_repo_dir = os.path.abspath(os.path.join(script_dir, '..', 'InSPyReNet-stable-projectorz'))

    # Path to Inference.py inside that repo
    inference_script = os.path.join(inspyre_repo_dir, 'run', 'Inference.py')
    if not os.path.isfile(inference_script):
        print(f"[ERROR] Could not find 'Inference.py' at: {inference_script}")
        sys.exit(1)

    # Path to config - e.g., "configs/InSPyReNet_SwinB.yaml"
    # Adjust if you prefer a different model config
    config_path = os.path.join(inspyre_repo_dir, 'configs', 'InSPyReNet_SwinB.yaml')
    if not os.path.isfile(config_path):
        print(f"[ERROR] Could not find config file at: {config_path}")
        sys.exit(1)

    # Make sure input/output exist
    if not os.path.isdir(input_dir):
        print(f"[ERROR] Input directory not found: {input_dir}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    # We'll check if there's at least 1 file in input:
    exts = (".png", ".jpg", ".jpeg", ".bmp", ".tiff")
    images_in_input = [
        f for f in os.listdir(input_dir)
        if os.path.splitext(f.lower())[1] in exts
    ]
    if not images_in_input:
        print(f"No images found in {input_dir}. Aborting.")
        sys.exit(1)

    # Now build the command.
    # The '--type rgba' argument means we want an alpha channel (transparent background).
    # If you have a GPU and want to use it, leave `--gpu`.
    # If you want to speed it up slightly, leave `--jit`.
    # If you only have CPU, remove `--gpu --jit`.
    command = [
        sys.executable,  # same Python interpreter
        inference_script,
        '--config', config_path,
        '--source', input_dir,
        '--dest', output_dir,
        '--type', 'rgba',
        '--verbose',
        '--gpu',
        '--jit',
    ]

    print("Found these images in 'input':", images_in_input)
    print("\nRunning InSPyReNet Inference script...")

    try:
        subprocess.run(command, check=True)
        print("\nDone. Check your 'output' folder for results.")
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Inference script failed with return code {e.returncode}.")
        sys.exit(e.returncode)

if __name__ == '__main__':
    main()
