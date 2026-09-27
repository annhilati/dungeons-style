import beet
import beet.contrib.optifine as of
import javaproperties
from pathlib import Path

BUILD = Path(__file__).parent / "build"


def beet_default(ctx: beet.Context):

    rp = beet.ResourcePack(
        path="src",
        extend_namespace=(
            of.OptifineProperties,
            of.OptifineTexture
        )
    )

    # Step 1

    for prop_id in rp[of.OptifineProperties].keys():
        prop_file = rp[of.OptifineProperties][prop_id]

        data = javaproperties.loads(prop_file.text)

        if (biomes := data.get("biomes")):
            biomes = biomes.split(" ")

    rp.save(BUILD / "out", overwrite=True)