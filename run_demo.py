import albumentations as A
from albumentations.pytorch import ToTensorV2
from demo_dataloader import get_loader
from tensordict_packages.collate_wrapper import Collate_Fn
from tensordict_packages.utils_and_toolbox import put_batch_on_device


batch_size = 8
image_size = 256
DEVICE = 'cuda:0'
path_to_dataset_folder = None
transform = A.Compose(
    [
        # if use_tensordict, probability based transforms must be defined here instead of in Dataset, and are inputted into Collate_Fn.
        A.Rotate(limit=0.5, p=0.5),
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.5),
        ToTensorV2(), # <--- must include ToTensorV2().
    ], is_check_shapes=False,
    #additional_targets={'image': 'image', 'mask': 'mask'} # can leave as commented out since Collate_Fn handles this.
)


for use_tensordict, type_inputted_into_torch_DataLoader in enumerate(['torch.utils.data.Dataset <--- baseline', 'tensordict.TensorDict.MemoryMappedTensor <--- what the tensordict_packages wraps Dataset with']):
    loader = get_loader(
        batch_size=batch_size,
        image_size=image_size,
        DEVICE=DEVICE,
        path_to_dataset_folder=path_to_dataset_folder,
        use_tensordict=use_tensordict,
        #collate_fn=None, <--- can be None if not use_tensordict.
        collate_fn=Collate_Fn(
            batch_size=batch_size,
            DEVICE=DEVICE,
            #transform=None, # <--- can be None if use_tensordict and there are no probability based transforms.
            transform=transform, # <--- if use_tensordict, can input probability based transforms (which cannot be in Dataset).
        ),
    )


    print(f'\n>> [RUNNING MOCH EPOCH] {type_inputted_into_torch_DataLoader}\n')
    from tqdm import tqdm
    for i, batch in tqdm(enumerate(loader), total=len(loader)):
        # var names returned from Dataset.__getitem__ and Albumentations.Compose.addional_targets.keys() must all match if use_tensordict.
        # var names here below do not matter for tensordict memory mapping.
        image, mask, mask_2d, some_binary_label, some_multi_labels = put_batch_on_device(batch=batch, DEVICE=DEVICE)
        # prediction = model(image)
        # ...
        # ...
        # ...

    print('\n')
