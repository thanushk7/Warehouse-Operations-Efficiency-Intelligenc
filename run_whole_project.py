import subprocess
import os
import sys




print("\nStarting Full Procurement Analytics Pipeline...\n")

base = os.getcwd()

modules_folder = os.path.join(base, "module")
modules = [
    "module1.py",
    "module2.py",
    "module3.py",
    "module4.py",
    "module5.py",
    "module6.py",
    "module7.py",
    "module8.py",
    "module9.py",
    "module10.py"
]
for module in modules:
    
    module_path = os.path.join(modules_folder, module)

    print(f"\nRunning {module} ...")

    subprocess.run([sys.executable, module_path])

print("\nAll Modules Executed Successfully ✅")