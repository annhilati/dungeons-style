import beet
import beet.contrib.optifine as of
import javaproperties
from pathlib import Path

from lib import BetterLeaves

BUILD = Path(__file__).parent / "build"


def beet_default(ctx: beet.Context):

    rp = beet.ResourcePack(
        name="Annhilati's Dungeons Style",
        path="src",
        extend_namespace=(
            of.OptifineProperties,
            of.OptifineTexture
        )
    )

    # Step 0

    leaf_pack = BetterLeaves.get_pack() 
    rp.merge(leaf_pack)
    print(f"rp models count: {len(rp.models)}")

    # Step 1

    for prop_id in rp[of.OptifineProperties].keys():
        prop_file = rp[of.OptifineProperties][prop_id]

        data = javaproperties.loads(prop_file.text)

        if (biomes := data.get("biomes")):
            biomes = biomes.split(" ")


    rp.save(BUILD, overwrite=True)