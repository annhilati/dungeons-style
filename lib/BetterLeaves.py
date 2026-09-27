import subprocess
import beet
from pathlib import Path
import os

def get_pack():
    BetterLeaves = Path(__file__).parent / 'BetterLeaves'
    
    command = ['python', 'gen_pack.py', '9.5', '§aVanilla', 'Edition', '--minify']
    
    # Zwingt den Subprocess (gen_pack.py), UTF-8 anstatt des Windows-Standard-Encodings zu nutzen
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    
    result = subprocess.run(
        command, 
        cwd=BetterLeaves, 
        capture_output=True, 
        text=True,
        env=env
    )

    rp = beet.ResourcePack(path=BetterLeaves / "Better-Leaves-9.5.zip", zipped=True)
    
    # Reset the BetterLeaves git submodule komplett, nachdem das Pack geladen wurde
    subprocess.run(['git', 'restore', '.'], cwd=BetterLeaves)
    subprocess.run(['git', 'clean', '-fd'], cwd=BetterLeaves)
    # Verhindere, dass die pack.mcmeta/pack.png vom Sub-Pack dein Hauptpack überschreiben
    rp.extra.pop("pack.mcmeta", None)
    rp.extra.pop("pack.png", None)
    return rp