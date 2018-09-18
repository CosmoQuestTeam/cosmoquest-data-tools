import imgaug as ia
from imgaug import augmenters as iaa

# There is no logical way of naming these...
# So I'm using https://killercup.github.io/codenamer/ with: Nope - US Submarine Classes - Greek Gods

def grayback_gaia():
    sequence = iaa.Sequential([
        iaa.Fliplr(0.5),
        iaa.Flipud(0.5),
        iaa.Sometimes(0.9, iaa.Affine(
            scale=[1, 2.5],
            translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},
            rotate=(-10, 10),
            order=1,
            cval=(0, 0),
            mode="constant"
        )),
        iaa.Sometimes(0.5, iaa.ContrastNormalization((0.5, 1.5))),
        iaa.Sometimes(0.5, 
            iaa.OneOf(
                [
                    iaa.Add((-50, 50)),
                    iaa.Multiply((0.5, 1.5))         
                ]
            )        
        ),
        iaa.Sometimes(0.2, 
            iaa.OneOf(
                [
                    iaa.GaussianBlur(sigma=(0.0, 4.0)),
                    iaa.Sharpen(alpha=(0.0, 1.0), lightness=(0.75, 2.0))
                ]
            )      
        ),
        iaa.Sometimes(0.1, iaa.AdditiveGaussianNoise(scale=(0, 0.1 * 255))),
        iaa.Sometimes(0.1,
        iaa.OneOf(
                [
                    iaa.Dropout(p=(0, 0.2)),
                    iaa.CoarseDropout((0.0, 0.025), size_percent=(0.08)),
                    iaa.SaltAndPepper(p=(0,0.2)),
                    iaa.CoarseSaltAndPepper((0.0, 0.025), size_percent=(0.08))
                ]
            )          
        )
    ], random_order=False)

    return sequence


IMAGE_AUGMENTATION_PIPELINES = {
    "DEFAULT": grayback_gaia,
    "GRAYBACK_GAIA": grayback_gaia
}
