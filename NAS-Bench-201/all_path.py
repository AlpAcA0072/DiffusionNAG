PATH = '/zhaoyifan/DiffusionNAG/NAS-Bench-201'
import os

SCORENET_CKPT_PATH=os.path.join(PATH, "./checkpoints/scorenet/checkpoint.pth.tar")
META_SURROGATE_CKPT_PATH=os.path.join(PATH, "./checkpoints/meta_surrogate/checkpoint.pth.tar")
META_SURROGATE_UNNOISED_CKPT_PATH = os.path.join(PATH, "./checkpoints/meta_surrogate/unnoised_checkpoint.pth.tar")
NASBENCH201=os.path.join(PATH, "./data/transfer_nag/nasbench201.pt")
NASBENCH201_INFO=os.path.join(PATH, "./data/transfer_nag/nasbench201_info.pt")
META_TEST_PATH=os.path.join(PATH, "./data/transfer_nag/test")
RAW_DATA_PATH=os.path.join(PATH, "./data/raw_data")
DATA_PATH = os.path.join(PATH, "./data/transfer_nag")
